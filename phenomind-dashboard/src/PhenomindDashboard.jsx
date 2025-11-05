import React, { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { Button } from "./components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "./components/ui/tabs";
import { Progress } from "./components/ui/progress";
import { Badge } from "./components/ui/badge";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { Avatar, AvatarFallback, AvatarImage } from "./components/ui/avatar";
import { AlertTriangle, Activity, Brain, ShieldCheck, ShieldAlert, Bell, Calendar as CalIcon, Search, TrendingUp, LineChart as LineIcon, Users, Lock, Stethoscope, Info } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, Tooltip as RTooltip, CartesianGrid, ResponsiveContainer, AreaChart, Area, BarChart, Bar } from "recharts";
import { motion } from "framer-motion";

// --- Fake demo data ---
const days = Array.from({ length: 30 }).map((_, i) => {
  const d = new Date();
  d.setDate(d.getDate() - (29 - i));
  const label = d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
  return label;
});

const trendData = days.map((d, i) => ({
  day: d,
  mood: 60 + Math.sin(i / 4) * 10 + (i > 20 ? -6 : 0), // scaled 0-100
  sleep: 7 + Math.sin(i / 5) * 0.6 + (i > 22 ? -0.8 : 0), // hours
  hrv: 45 + Math.cos(i / 6) * 8 + (i > 20 ? -6 : 0), // ms
  activity: 7000 + Math.sin(i / 3) * 1500 + (i > 24 ? -2200 : 0), // steps
}));

const forecastData = days.slice(20).map((d, i) => ({
  day: d,
  risk: Math.max(4, Math.min(96, 35 + i * 2.5 + (i > 6 ? 6 : 0) + Math.sin(i) * 4)),
}));

const population = [
  { disorder: "MDD", patients: 124, highRisk: 18 },
  { disorder: "Bipolar", patients: 62, highRisk: 9 },
  { disorder: "Anxiety", patients: 210, highRisk: 22 },
  { disorder: "Schizoaffective", patients: 14, highRisk: 3 },
];

const timeline = [
  { date: "Apr 3", label: "Medication dose ↑ (Sertraline 50→75mg)", type: "med" },
  { date: "Apr 6", label: "Sleep irregularity detected (avg 5.8h; baseline 7.1h)", type: "alert" },
  { date: "Apr 10", label: "PHQ-9 via app: 12 (↑2)", type: "survey" },
  { date: "Apr 13", label: "Reduced mobility (−32% steps vs baseline)", type: "alert" },
  { date: "Apr 15", label: "Televisit completed; therapy referral placed", type: "visit" },
];

function RiskChip({ score }) {
  const level = score < 33 ? "Low" : score < 66 ? "Moderate" : "High";
  const Icon = level === "High" ? ShieldAlert : ShieldCheck;
  const color = level === "High" ? "bg-red-100 text-red-700" : level === "Moderate" ? "bg-amber-100 text-amber-700" : "bg-emerald-100 text-emerald-700";
  return (
    <Badge className={`rounded-full px-3 py-1 ${color} font-medium`}> 
      <Icon className="mr-1 h-4 w-4" />{level} • {Math.round(score)}%
    </Badge>
  );
}

function Stat({ title, value, delta, icon: Icon }) {
  return (
    <Card className="rounded-2xl shadow-sm">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2"><Icon className="h-4 w-4" />{title}</CardTitle>
        {delta && <span className={`text-xs ${delta.startsWith("+") ? "text-emerald-600" : "text-rose-600"}`}>{delta}</span>}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-semibold">{value}</div>
      </CardContent>
    </Card>
  );
}

function TrendCard({ title, dataKey, unit, description }) {
  return (
    <Card className="rounded-2xl shadow-sm">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2"><LineIcon className="h-4 w-4" />{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-40">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={trendData} margin={{ left: 10, right: 10 }}>
              <defs>
                <linearGradient id={`g-${String(dataKey)}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopOpacity={0.35}/>
                  <stop offset="95%" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" hide />
              <YAxis hide />
              <RTooltip formatter={(v) => `${v}${unit ?? ""}`} />
              <Area type="monotone" dataKey={String(dataKey)} strokeWidth={2} fillOpacity={1} fill={`url(#g-${String(dataKey)})`} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        {description && <p className="text-xs text-muted-foreground mt-2">{description}</p>}
      </CardContent>
    </Card>
  );
}

function AISummary() {
  return (
    <Card className="rounded-2xl shadow-sm border-emerald-100">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2"><Brain className="h-4 w-4" />AI Summary</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3 text-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldAlert className="h-4 w-4" />
            <span>Relapse likelihood (14 days)</span>
          </div>
          <RiskChip score={58} />
        </div>
        <Progress value={58} className="h-2" />
        <ul className="list-disc pl-5 text-muted-foreground">
          <li>Primary drivers: sleep irregularity, reduced HRV, mobility ↓</li>
          <li>Protective factor: consistent therapy attendance</li>
        </ul>
        <div className="pt-1">
          <Label className="text-xs uppercase tracking-wide text-muted-foreground">Recommendations</Label>
          <div className="mt-2 grid grid-cols-1 gap-2 md:grid-cols-2">
            <Button variant="secondary" className="justify-start"><Stethoscope className="h-4 w-4 mr-2"/>Consider sleep-focused CBT-I referral</Button>
            <Button variant="secondary" className="justify-start"><Activity className="h-4 w-4 mr-2"/>Review HRV and medication timing</Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function PatientHeader() {
  return (
    <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
      <div className="flex items-center gap-3">
        <Avatar className="h-10 w-10">
          <AvatarImage src="https://i.pravatar.cc/100?img=5" />
          <AvatarFallback>JD</AvatarFallback>
        </Avatar>
        <div>
          <h1 className="text-xl font-semibold">Jane Doe</h1>
          <p className="text-xs text-muted-foreground">MDD • Sertraline 75mg • Last visit: 10 days ago</p>
        </div>
      </div>
      <div className="flex gap-2 items-center">
        <div className="hidden md:flex items-center gap-2">
          <CalIcon className="h-4 w-4"/>
          <span className="text-sm text-muted-foreground">Range: 30 days</span>
        </div>
        <div className="flex items-center gap-2">
          <Input placeholder="Search patients" className="w-52"/>
          <Button variant="outline"><Search className="h-4 w-4 mr-1"/>Search</Button>
          <Button><Bell className="h-4 w-4 mr-1"/>Alerts</Button>
        </div>
      </div>
    </div>
  );
}

function TimelineCard() {
  const dot = (t) => t === "alert" ? "bg-rose-500" : t === "med" ? "bg-indigo-500" : t === "visit" ? "bg-emerald-500" : "bg-amber-500";
  return (
    <Card className="rounded-2xl shadow-sm">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2"><TrendingUp className="h-4 w-4" />Patient Timeline</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="relative pl-3">
          <div className="absolute left-3 top-0 bottom-0 w-px bg-muted" />
          <ul className="space-y-4">
            {timeline.map((t, i) => (
              <li key={i} className="relative">
                <div className={`absolute -left-[7px] top-1 h-3 w-3 rounded-full ${dot(t.type)}`} />
                <div className="ml-4">
                  <div className="text-xs text-muted-foreground">{t.date}</div>
                  <div className="text-sm">{t.label}</div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </CardContent>
    </Card>
  );
}

function PopulationView() {
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
      <Card className="rounded-2xl shadow-sm lg:col-span-2">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2"><Users className="h-4 w-4"/>Cohort Risk Overview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={population}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="disorder" />
                <YAxis />
                <RTooltip />
                <Bar dataKey="patients" name="Patients" />
                <Bar dataKey="highRisk" name="High Risk" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
      <Card className="rounded-2xl shadow-sm">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2"><Lock className="h-4 w-4"/>Privacy & Compliance</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-sm">
          <div className="flex items-center justify-between"><span>Federated learning status</span><Badge variant="secondary">Active</Badge></div>
          <div className="flex items-center justify-between"><span>Differential privacy</span><Badge variant="outline">ε = 2.0</Badge></div>
          <div className="flex items-center justify-between"><span>HIPAA compliance</span><Badge className="bg-emerald-100 text-emerald-700">Verified</Badge></div>
          <div className="flex items-center justify-between"><span>FDA pathway</span><Badge>CDS → SaMD</Badge></div>
          <p className="text-xs text-muted-foreground">No raw data leaves sites. Only encrypted model updates are shared.</p>
        </CardContent>
      </Card>
    </div>
  );
}

function ForecastCard() {
  return (
    <Card className="rounded-2xl shadow-sm">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2"><AlertTriangle className="h-4 w-4" />Risk Forecast (next 30 days)</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-40">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={forecastData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" hide />
              <YAxis hide />
              <RTooltip formatter={(v) => `${Math.round(v)}%`} />
              <Line type="monotone" dataKey="risk" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}

export default function Component() {
  const [tab, setTab] = useState("patient");

  return (
    <div className="p-6 md:p-8 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <motion.div initial={{ opacity: 0, y: -6 }} animate={{ opacity: 1, y: 0 }} className="text-2xl font-semibold">
            PhenoMind Dashboard
          </motion.div>
          <Badge variant="secondary" className="ml-2">Clinician</Badge>
        </div>
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <Info className="h-4 w-4"/> Demo mock data for layout preview
        </div>
      </div>

      <Tabs value={tab} onValueChange={setTab} className="w-full">
        <TabsList className="grid grid-cols-3 w-full md:w-auto">
          <TabsTrigger value="patient">Patient</TabsTrigger>
          <TabsTrigger value="insights">AI Insights</TabsTrigger>
          <TabsTrigger value="population">Population</TabsTrigger>
        </TabsList>

        {/* Patient tab */}
        <TabsContent value="patient" className="space-y-6">
          <PatientHeader />

          {/* Top stats */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <Stat title="Risk Level" value={<RiskChip score={58} />} icon={ShieldAlert} />
            <Stat title="Avg Sleep (7d)" value={`6.3 h`} delta="-0.8h" icon={CalIcon} />
            <Stat title="HRV (7d)" value={`42 ms`} delta="-5 ms" icon={Activity} />
            <Stat title="Activity (7d)" value={`6,120 steps`} delta="-18%" icon={TrendingUp} />
          </div>

          {/* Trends */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <TrendCard title="Mood (self-report)" dataKey="mood" />
            <TrendCard title="Sleep duration" dataKey="sleep" unit=" h" />
            <TrendCard title="HRV (RMSSD)" dataKey="hrv" unit=" ms" />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <ForecastCard />
            <AISummary />
            <TimelineCard />
          </div>
        </TabsContent>

        {/* Insights tab */}
        <TabsContent value="insights" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <Card className="rounded-2xl shadow-sm lg:col-span-2">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2"><Brain className="h-4 w-4"/>Top Biomarker Drivers</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-56">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={[{ f: "Sleep irregularity", w: 0.38 }, { f: "HRV ↓", w: 0.29 }, { f: "Mobility ↓", w: 0.21 }, { f: "Screen-time ↑ late", w: 0.12 }]} layout="vertical">
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" domain={[0, 0.5]} />
                      <YAxis type="category" dataKey="f" width={150} />
                      <RTooltip formatter={(v) => `${Math.round(v*100)}% importance`} />
                      <Bar dataKey="w" name="Importance" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
            <Card className="rounded-2xl shadow-sm">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2"><Stethoscope className="h-4 w-4"/>Treatment Scenarios</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm">
                <div className="flex items-center justify-between"><span>Continue current plan</span><Badge variant="secondary">Risk ~58%</Badge></div>
                <div className="flex items-center justify-between"><span>Add CBT-I</span><Badge>Risk ~44%</Badge></div>
                <div className="flex items-center justify-between"><span>Adjust dose timing</span><Badge>Risk ~49%</Badge></div>
                <p className="text-xs text-muted-foreground">Modeled outcomes from patient-specific digital twin.</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Population tab */}
        <TabsContent value="population" className="space-y-6">
          <PopulationView />
        </TabsContent>
      </Tabs>
    </div>
  );
}
