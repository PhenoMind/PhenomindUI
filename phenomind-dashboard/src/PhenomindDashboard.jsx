import React, { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card.jsx";
import { Button } from "./components/ui/button.jsx";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "./components/ui/tabs.jsx";
import { Progress } from "./components/ui/progress.jsx";
import { Badge } from "./components/ui/badge.jsx";
import { Input } from "./components/ui/input.jsx";
import { Label } from "./components/ui/label.jsx";
import { Avatar, AvatarFallback, AvatarImage } from "./components/ui/avatar.jsx";
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
  { site: "Mass General Hospital", patients: 324, highRisk: 45, modelAccuracy: 89 },
  { site: "Johns Hopkins", patients: 298, highRisk: 38, modelAccuracy: 92 },
  { site: "Mayo Clinic", patients: 412, highRisk: 67, modelAccuracy: 87 },
  { site: "Cleveland Clinic", patients: 256, highRisk: 31, modelAccuracy: 91 },
];

const disorderBreakdown = [
  { disorder: "Depression", totalPatients: 645, highRisk: 89, networkSites: 4 },
  { disorder: "Bipolar", totalPatients: 298, highRisk: 47, networkSites: 4 },
  { disorder: "Anxiety", totalPatients: 423, highRisk: 52, networkSites: 4 },
  { disorder: "PTSD", totalPatients: 124, highRisk: 18, networkSites: 3 },
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
    <Badge className={`rounded-full px-5 py-3 ${color} font-semibold text-lg`}> 
      <Icon className="mr-2 h-6 w-6" />{level} • {Math.round(score)}%
    </Badge>
  );
}

function Stat({ title, value, delta, icon: Icon }) {
  return (
    <Card className="rounded-2xl shadow-sm">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><Icon className="h-6 w-6" />{title}</CardTitle>
        {delta && <span className={`text-lg font-semibold ${delta.startsWith("+") ? "text-emerald-600" : "text-rose-600"}`}>{delta}</span>}
      </CardHeader>
      <CardContent>
        <div className="text-4xl font-semibold text-center">{value}</div>
      </CardContent>
    </Card>
  );
}

function TrendCard({ title, dataKey, unit, description }) {
  return (
    <Card className="rounded-2xl shadow-sm">
      <CardHeader className="pb-2">
        <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><LineIcon className="h-6 w-6" />{title}</CardTitle>
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
              <RTooltip 
                formatter={(v) => `${v}${unit ?? ""}`}
                contentStyle={{
                  backgroundColor: '#ffffff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                  fontSize: '16px'
                }}
              />
              <Area type="monotone" dataKey={String(dataKey)} strokeWidth={2} fillOpacity={1} fill={`url(#g-${String(dataKey)})`} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        {description && <p className="text-base text-muted-foreground mt-2">{description}</p>}
      </CardContent>
    </Card>
  );
}

function AISummary() {
  return (
    <Card className="rounded-2xl shadow-sm border-emerald-100">
      <CardHeader className="pb-2">
        <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><Brain className="h-6 w-6" />AI Summary</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3 text-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldAlert className="h-6 w-6" />
            <span className="font-medium">Relapse likelihood (14 days)</span>
          </div>
          <RiskChip score={58} />
        </div>
        <Progress value={58} className="h-4" />
        <ul className="list-disc pl-6 text-muted-foreground text-lg space-y-1">
          <li>Primary drivers: sleep irregularity, reduced HRV, mobility ↓</li>
          <li>Protective factor: consistent therapy attendance</li>
        </ul>
        <div className="pt-2">
          <Label className="text-base uppercase tracking-wide text-muted-foreground font-semibold">Recommendations</Label>
          <div className="mt-3 grid grid-cols-1 gap-3 md:grid-cols-2">
            <Button variant="secondary" className="justify-start text-base py-3"><Stethoscope className="h-6 w-6 mr-2"/>Consider sleep-focused CBT-I referral</Button>
            <Button variant="secondary" className="justify-start text-base py-3"><Activity className="h-6 w-6 mr-2"/>Review HRV and medication timing</Button>
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
        <Avatar className="h-16 w-16">
          <AvatarImage src="https://i.pravatar.cc/100?img=5" />
          <AvatarFallback className="text-xl font-semibold">JD</AvatarFallback>
        </Avatar>
        <div>
          <h1 className="text-3xl font-semibold">Jane Doe</h1>
          <p className="text-lg text-muted-foreground">MDD • Sertraline 75mg • Last visit: 10 days ago</p>
        </div>
      </div>
      <div className="flex gap-3 items-center">
        <div className="hidden md:flex items-center gap-2">
          <CalIcon className="h-6 w-6"/>
          <span className="text-lg text-muted-foreground">Range: 30 days</span>
        </div>
        <div className="flex items-center gap-3">
          <Input placeholder="Search patients" className="w-52 text-lg py-3"/>
          <Button variant="outline" className="text-lg py-3 px-4"><Search className="h-6 w-6 mr-2"/>Search</Button>
          <Button className="text-lg py-3 px-4"><Bell className="h-6 w-6 mr-2"/>Alerts</Button>
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
        <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><TrendingUp className="h-6 w-6" />Patient Timeline</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="relative pl-4">
          <div className="absolute left-4 top-0 bottom-0 w-px bg-muted" />
          <ul className="space-y-5">
            {timeline.map((t, i) => (
              <li key={i} className="relative">
                <div className={`absolute -left-[8px] top-1 h-4 w-4 rounded-full ${dot(t.type)}`} />
                <div className="ml-6">
                  <div className="text-base text-muted-foreground font-medium">{t.date}</div>
                  <div className="text-lg">{t.label}</div>
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
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      {/* Network Overview - Visual Impact */}
      <Card className="rounded-2xl shadow-sm lg:col-span-2">
        <CardHeader className="pb-4">
          <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><Users className="h-6 w-6"/>Network Overview</CardTitle>
        </CardHeader>
        <CardContent>
          {/* Big Numbers First */}
          <div className="grid grid-cols-4 gap-4 mb-6">
            <div className="text-center">
              <div className="text-6xl font-bold text-blue-600">4</div>
              <div className="text-xl text-muted-foreground font-semibold">Premier Hospitals</div>
            </div>
            <div className="text-center">
              <div className="text-6xl font-bold text-emerald-600">1,490</div>
              <div className="text-xl text-muted-foreground font-semibold">Total Patients</div>
            </div>
            <div className="text-center">
              <div className="text-6xl font-bold text-red-600">181</div>
              <div className="text-xl text-muted-foreground font-semibold">High Risk</div>
            </div>
            <div className="text-center">
              <div className="text-6xl font-bold text-amber-600">4</div>
              <div className="text-xl text-muted-foreground font-semibold">Conditions</div>
            </div>
          </div>

          {/* Visual Network Diagram */}
          <div className="relative bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 mb-4">
            <svg width="100%" height="380" viewBox="0 0 700 380" className="overflow-visible">
              {/* Connection Lines - Animated */}
              <defs>
                <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.8"/>
                  <stop offset="100%" stopColor="#6366f1" stopOpacity="0.5"/>
                </linearGradient>
              </defs>
              
              <g stroke="url(#lineGradient)" strokeWidth="4" strokeDasharray="10,8">
                <line x1="350" y1="190" x2="140" y2="100">
                  <animate attributeName="stroke-dashoffset" values="0;-36" dur="3s" repeatCount="indefinite"/>
                </line>
                <line x1="350" y1="190" x2="560" y2="100">
                  <animate attributeName="stroke-dashoffset" values="0;-36" dur="3s" begin="0.5s" repeatCount="indefinite"/>
                </line>
                <line x1="350" y1="190" x2="140" y2="280">
                  <animate attributeName="stroke-dashoffset" values="0;-36" dur="3s" begin="1s" repeatCount="indefinite"/>
                </line>
                <line x1="350" y1="190" x2="560" y2="280">
                  <animate attributeName="stroke-dashoffset" values="0;-36" dur="3s" begin="1.5s" repeatCount="indefinite"/>
                </line>
              </g>
              
              {/* Central PhenoMind Hub */}
              <g>
                <rect x="270" y="150" width="160" height="80" rx="16" fill="#3b82f6" opacity="0.95" stroke="#1e40af" strokeWidth="3"/>
                <text x="350" y="180" textAnchor="middle" fill="white" fontSize="20" fontWeight="700">
                  PhenoMind
                </text>
                <text x="350" y="205" textAnchor="middle" fill="white" fontSize="16" fontWeight="600">
                  Federated AI
                </text>
              </g>
              
              {/* Hospital Network Nodes */}
              <g>
                {/* Mass General Hospital */}
                <rect x="60" y="60" width="160" height="80" rx="12" fill="#10b981" opacity="0.95" stroke="#059669" strokeWidth="3"/>
                <text x="140" y="95" textAnchor="middle" fill="white" fontSize="16" fontWeight="700">Mass General</text>
                <text x="140" y="115" textAnchor="middle" fill="white" fontSize="16" fontWeight="700">Hospital</text>
                <text x="140" y="165" textAnchor="middle" fill="#1f2937" fontSize="18" fontWeight="700">324 patients</text>
                
                {/* Johns Hopkins */}
                <rect x="480" y="60" width="160" height="80" rx="12" fill="#8b5cf6" opacity="0.95" stroke="#7c3aed" strokeWidth="3"/>
                <text x="560" y="95" textAnchor="middle" fill="white" fontSize="16" fontWeight="700">Johns Hopkins</text>
                <text x="560" y="115" textAnchor="middle" fill="white" fontSize="16" fontWeight="700">University</text>
                <text x="560" y="165" textAnchor="middle" fill="#1f2937" fontSize="18" fontWeight="700">298 patients</text>
                
                {/* Mayo Clinic */}
                <rect x="60" y="240" width="160" height="80" rx="12" fill="#f59e0b" opacity="0.95" stroke="#d97706" strokeWidth="3"/>
                <text x="140" y="275" textAnchor="middle" fill="white" fontSize="16" fontWeight="700">Mayo Clinic</text>
                <text x="140" y="295" textAnchor="middle" fill="white" fontSize="16" fontWeight="700">Rochester</text>
                <text x="140" y="345" textAnchor="middle" fill="#1f2937" fontSize="18" fontWeight="700">412 patients</text>
                
                {/* Cleveland Clinic */}
                <rect x="480" y="240" width="160" height="80" rx="12" fill="#ef4444" opacity="0.95" stroke="#dc2626" strokeWidth="3"/>
                <text x="560" y="275" textAnchor="middle" fill="white" fontSize="16" fontWeight="700">Cleveland</text>
                <text x="560" y="295" textAnchor="middle" fill="white" fontSize="16" fontWeight="700">Clinic</text>
                <text x="560" y="345" textAnchor="middle" fill="#1f2937" fontSize="18" fontWeight="700">256 patients</text>
              </g>
            </svg>
          </div>

          {/* Condition Breakdown with High Risk */}
          <div className="grid grid-cols-2 gap-4">
            <div className="flex justify-between items-center p-5 bg-gray-50 rounded-lg">
              <div>
                <div className="text-xl font-semibold">Depression</div>
                <div className="text-lg text-red-600 font-semibold">89 high risk</div>
              </div>
              <span className="text-3xl font-bold text-indigo-600">645</span>
            </div>
            <div className="flex justify-between items-center p-5 bg-gray-50 rounded-lg">
              <div>
                <div className="text-xl font-semibold">Anxiety</div>
                <div className="text-lg text-red-600 font-semibold">52 high risk</div>
              </div>
              <span className="text-3xl font-bold text-indigo-600">423</span>
            </div>
            <div className="flex justify-between items-center p-5 bg-gray-50 rounded-lg">
              <div>
                <div className="text-xl font-semibold">Bipolar</div>
                <div className="text-lg text-red-600 font-semibold">47 high risk</div>
              </div>
              <span className="text-3xl font-bold text-indigo-600">298</span>
            </div>
            <div className="flex justify-between items-center p-5 bg-gray-50 rounded-lg">
              <div>
                <div className="text-xl font-semibold">PTSD</div>
                <div className="text-lg text-red-600 font-semibold">18 high risk</div>
              </div>
              <span className="text-3xl font-bold text-indigo-600">124</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Federated Learning */}
      <Card className="rounded-2xl shadow-sm">
        <CardHeader className="pb-4">
          <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><Lock className="h-6 w-6"/>Federated Learning</CardTitle>
        </CardHeader>
        <CardContent className="space-y-5">
          {/* High Risk Alert */}
          <div className="bg-red-50 border border-red-200 rounded-lg p-5 mb-5">
            <div className="flex items-center gap-3 mb-3">
              <AlertTriangle className="h-7 w-7 text-red-600" />
              <span className="font-semibold text-red-700 text-xl">High Risk Alert</span>
            </div>
            <div className="text-lg text-red-700">
              <strong>181 patients</strong> across network flagged as high risk for relapse in next 14 days
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-4xl font-semibold text-emerald-600">89.7%</div>
              <div className="text-lg text-muted-foreground">Model Accuracy</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-semibold text-indigo-600">4</div>
              <div className="text-lg text-muted-foreground">Active Sites</div>
            </div>
          </div>
          
          <div className="space-y-4 pt-2">
            <div className="flex items-center justify-between">
              <span className="text-xl text-foreground">Privacy level</span>
              <Badge variant="outline" className="text-lg py-2 px-3">ε = 2.0</Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xl text-foreground">HIPAA compliance</span>
              <Badge className="bg-emerald-100 text-emerald-700 text-lg py-2 px-3">Verified</Badge>
            </div>
          </div>

          <div className="pt-4">
            <div className="flex items-center justify-between text-lg text-muted-foreground mb-3">
              <span>Data sharing</span>
              <span>Conservative</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4">
              <div className="bg-blue-500 h-4 rounded-full" style={{ width: '35%' }}></div>
            </div>
            <p className="text-base text-muted-foreground mt-2">Higher sharing = Better accuracy</p>
          </div>

          <div className="pt-4 border-t border-gray-100">
            <p className="text-lg text-muted-foreground">Encrypted model updates shared across sites. Raw patient data never leaves hospitals.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function ForecastCard() {
  return (
    <Card className="rounded-2xl shadow-sm">
      <CardHeader className="pb-2">
        <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><AlertTriangle className="h-6 w-6" />Risk Forecast (next 30 days)</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-40">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={forecastData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" hide />
              <YAxis hide />
              <RTooltip 
                formatter={(v) => `${Math.round(v)}%`}
                contentStyle={{
                  backgroundColor: '#ffffff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                  fontSize: '16px'
                }}
              />
              <Line type="monotone" dataKey="risk" strokeWidth={3} dot={false} />
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
    <div className="p-8 md:p-12 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <img 
            src="/logo.png" 
            alt="PhenoMind Logo" 
            className="h-12 w-12 object-contain"
          />
          <motion.div initial={{ opacity: 0, y: -6 }} animate={{ opacity: 1, y: 0 }} className="text-3xl font-semibold">
            PhenoMind Clinician Dashboard
          </motion.div>
        </div>
      </div>

      <Tabs value={tab} onValueChange={setTab} className="w-full">
        <TabsList className="grid grid-cols-3 w-full md:w-auto">
          <TabsTrigger value="patient" className="text-xl py-5 font-semibold">Patient</TabsTrigger>
          <TabsTrigger value="insights" className="text-xl py-5 font-semibold">AI Insights</TabsTrigger>
          <TabsTrigger value="population" className="text-xl py-5 font-semibold">Population</TabsTrigger>
        </TabsList>

        {/* Patient tab */}
        <TabsContent value="patient" className="space-y-8 pt-6">
          <PatientHeader />

          {/* Top stats */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <Stat title="Depression Risk Level" value={<RiskChip score={58} />} icon={ShieldAlert} />
            <Stat title="Avg Sleep (7d)" value={`6.3 h`} delta="-0.8h" icon={CalIcon} />
            <Stat title="Heart Rate Variability (HRV) (7d)" value={`42 ms`} delta="-5 ms" icon={Activity} />
            <Stat title="Activity (7d)" value={`6,120 steps`} delta="-18%" icon={TrendingUp} />
          </div>

          {/* Trends */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <TrendCard title="Mood (self-report)" dataKey="mood" />
            <TrendCard title="Sleep duration" dataKey="sleep" unit=" h" />
            <TrendCard title="Heart Rate Variability (HRV)" dataKey="hrv" unit=" ms" />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <ForecastCard />
            <AISummary />
            <TimelineCard />
          </div>
        </TabsContent>

        {/* Insights tab */}
        <TabsContent value="insights" className="space-y-8 pt-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <Card className="rounded-2xl shadow-sm lg:col-span-2">
              <CardHeader className="pb-2">
                <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><Brain className="h-6 w-6"/>Top Biomarker Drivers</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={[
                      { f: "Sleep irregularity", w: 0.38, fill: "#dc2626" }, 
                      { f: "HRV ↓", w: 0.29, fill: "#16a34a" }, 
                      { f: "Mobility ↓", w: 0.21, fill: "#8b5cf6" }, 
                      { f: "Screen-time ↑ late", w: 0.12, fill: "#06b6d4" }
                    ]} layout="vertical" margin={{ left: 10, right: 10, top: 10, bottom: 40 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis type="number" domain={[0, 0.5]} tick={{ fontSize: 16, fill: '#6b7280' }} 
                             label={{ value: 'Importance', position: 'insideBottom', offset: -5, style: { fontSize: '18px', fontWeight: '500', fill: '#374151' } }} />
                      <YAxis type="category" dataKey="f" width={200} tick={{ fontSize: 18, fontWeight: '500', fill: '#374151' }} />
                      <RTooltip 
                        formatter={(v) => `${Math.round(v*100)}% importance`}
                        contentStyle={{
                          backgroundColor: '#ffffff',
                          border: '1px solid #e5e7eb',
                          borderRadius: '8px',
                          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                          fontSize: '16px'
                        }}
                      />
                      <Bar dataKey="w" name="Importance" radius={[0, 4, 4, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
            <Card className="rounded-2xl shadow-sm">
              <CardHeader className="pb-2">
                <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><Stethoscope className="h-6 w-6"/>Depression Treatment Scenarios</CardTitle>
              </CardHeader>
              <CardContent className="space-y-5 text-xl">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-foreground">Continue current plan</span>
                  <div className="flex items-center gap-2 justify-center">
                    <Badge variant="secondary" className="text-xl px-5 py-3 font-semibold bg-gray-100 text-gray-700">58% Risk</Badge>
                    <span className="text-lg font-semibold text-gray-600">(+0%)</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="font-medium text-foreground">Add CBT-I</span>
                  <div className="flex items-center gap-2 justify-center">
                    <Badge className="text-xl px-5 py-3 bg-emerald-100 text-emerald-700 font-semibold">44% Risk</Badge>
                    <span className="text-lg font-semibold text-emerald-600">(-14%)</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="font-medium text-foreground">Adjust dose timing</span>
                  <div className="flex items-center gap-2 justify-center">
                    <Badge className="text-xl px-5 py-3 bg-blue-100 text-blue-700 font-semibold">49% Risk</Badge>
                    <span className="text-lg font-semibold text-blue-600">(-9%)</span>
                  </div>
                </div>
                <p className="text-lg text-muted-foreground mt-6">Depression relapse risk from patient-specific digital twin model.</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Population tab */}
        <TabsContent value="population" className="space-y-8 pt-6">
          <PopulationView />
        </TabsContent>
      </Tabs>
    </div>
  );
}
