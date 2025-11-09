import React, { useState, useEffect, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card.jsx";
import { Button } from "./components/ui/button.jsx";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "./components/ui/tabs.jsx";
import { Progress } from "./components/ui/progress.jsx";
import { Badge } from "./components/ui/badge.jsx";
import { Input } from "./components/ui/input.jsx";
import { Label } from "./components/ui/label.jsx";
import { Avatar, AvatarFallback, AvatarImage } from "./components/ui/avatar.jsx";
import { AlertTriangle, Activity, Brain, ShieldCheck, ShieldAlert, Bell, Calendar as CalIcon, Search, TrendingUp, LineChart as LineIcon, Users, Lock, Stethoscope } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, Tooltip as RTooltip, CartesianGrid, ResponsiveContainer, AreaChart, Area, BarChart, Bar } from "recharts";
import { motion } from "framer-motion";
import apiService from "./services/api.js";

// ... existing code for RiskChip, Stat, TrendCard, AISummary, TimelineCard, PopulationView, ForecastCard components ...

// Patient Sidebar Component
function PatientSidebar({ patients, selectedPatientId, onPatientSelect, searchQuery, setSearchQuery, filteredPatients }) {

  const getRiskColor = (score) => {
    if (score < 33) return "bg-emerald-100 text-emerald-700 border-emerald-200";
    if (score < 66) return "bg-amber-100 text-amber-700 border-amber-200";
    return "bg-red-100 text-red-700 border-red-200";
  };

  return (
    <div className="w-80 bg-white border-r border-gray-200 flex flex-col h-screen fixed left-0 top-0 overflow-hidden">
      {/* Sidebar Header */}
      <div className="p-6 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
        <div className="flex items-center gap-3 mb-4">
          <img 
            src="/logo.png" 
            alt="PhenoMind Logo" 
            className="h-10 w-10 object-contain"
          />
          <h2 className="text-xl font-semibold text-gray-900">Patients</h2>
        </div>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <Input
                  placeholder="Search patients..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 w-full"
                />
              </div>
      </div>

      {/* Patient List */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-4 space-y-3">
          {(filteredPatients || patients).map((patient) => {
            const isSelected = patient.id === selectedPatientId;
            return (
                  <button
                key={patient.id}
                onClick={() => onPatientSelect(patient.id)}
                className={`w-full text-left p-4 rounded-xl border-2 transition-all duration-200 hover:shadow-md ${
                  isSelected
                    ? "bg-blue-50 border-blue-300 shadow-md"
                    : "bg-white border-gray-200 hover:border-gray-300"
                }`}
              >
                <div className="flex items-start gap-3">
                  <Avatar className="h-12 w-12 flex-shrink-0">
                    <AvatarImage src={patient.avatar} />
                    <AvatarFallback className="text-sm font-semibold">{patient.initials}</AvatarFallback>
                    </Avatar>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2 mb-1">
                      <h3 className={`font-semibold text-base truncate ${isSelected ? "text-blue-900" : "text-gray-900"}`}>
                        {patient.name}
                      </h3>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{patient.disorderFull}</p>
                    <div className="flex items-center gap-2 flex-wrap">
                      <Badge 
                        className={`text-xs px-2 py-1 font-semibold border ${getRiskColor(patient.riskScore)}`}
                      >
                        {patient.riskScore < 33 ? "Low" : patient.riskScore < 66 ? "Moderate" : "High"} Risk
                    </Badge>
                      <span className="text-xs text-gray-500">• {patient.age} years</span>
                    </div>
                    <div className="mt-2 text-xs text-gray-500">
                      Last visit: {patient.lastVisit}
                    </div>
                  </div>
                </div>
                  </button>
            );
          })}
              </div>
            </div>

      {/* Sidebar Footer */}
      <div className="p-4 border-t border-gray-200 bg-gray-50">
        <div className="text-sm text-gray-600 text-center">
          <span className="font-semibold">{(filteredPatients || patients).length}</span> patient{(filteredPatients || patients).length !== 1 ? 's' : ''} found
        </div>
      </div>
    </div>
  );
}

// Simplified Patient Header (no dropdown)
function PatientHeader({ patient }) {
  return (
    <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
      <div className="flex items-center gap-4">
        <Avatar className="h-16 w-16">
          <AvatarImage src={patient.avatar} />
          <AvatarFallback className="text-xl font-semibold">{patient.initials}</AvatarFallback>
        </Avatar>
        <div>
          <h1 className="text-3xl font-semibold">{patient.name}</h1>
          <p className="text-lg text-muted-foreground">
            {patient.disorderFull} • {patient.medications.join(", ")} • Last visit: {patient.lastVisit}
          </p>
        </div>
      </div>
      <div className="flex gap-3 items-center">
        <div className="hidden md:flex items-center gap-2">
          <CalIcon className="h-6 w-6"/>
          <span className="text-lg text-muted-foreground">Range: 30 days</span>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" className="text-lg py-3 px-4"><Bell className="h-6 w-6 mr-2"/>Alerts</Button>
        </div>
      </div>
    </div>
  );
}

// Update ForecastCard to use patient data
function ForecastCard({ patient }) {
  if (!patient?.trendData || patient.trendData.length === 0) {
    return null;
  }
  const forecastData = patient.trendData.slice(20).map((d, i) => ({
    day: d.day,
    risk: Math.max(4, Math.min(96, patient.riskScore + i * 2.5 + (i > 6 ? 6 : 0) + Math.sin(i) * 4)),
  }));

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

// Update TrendCard to use patient data
function TrendCard({ title, dataKey, unit, description, data }) {
  return (
    <Card className="rounded-2xl shadow-sm">
      <CardHeader className="pb-2">
        <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><LineIcon className="h-6 w-6" />{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-40">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ left: 10, right: 10 }}>
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

// Update AISummary to use patient data and analytics
function AISummary({ patient, analytics }) {
  const drivers = analytics?.biomarkerDrivers || [];
  const recommendations = analytics?.recommendations || [];
  
  // Generate driver text from analytics
  const driverText = drivers.length > 0 
    ? drivers.map(d => {
        const importance = d.impact || d.importance || 0;
        const trend = d.direction || d.trend || '';
        const factor = d.factor || '';
        const arrow = trend === 'decreasing' ? '↓' : trend === 'increasing' ? '↑' : '';
        return `${factor} ${arrow} (${Math.round(importance * 100)}% impact)`;
      }).join(', ')
    : 'No significant drivers identified';
  
  // Get protective factors from patient data
  const protectiveFactors = [];
  if (patient?.ehr?.medications?.length > 0) {
    protectiveFactors.push('consistent medication adherence');
  }
  if (patient?.timeline?.some(t => t.type === 'visit')) {
    protectiveFactors.push('regular therapy attendance');
  }
  if (patient?.wearable?.steps_goal && patient?.trendData) {
    const recentSteps = patient.trendData.slice(-7).reduce((sum, d) => sum + d.activity, 0) / 7;
    if (recentSteps >= patient.wearable.steps_goal * 0.8) {
      protectiveFactors.push('maintaining activity goals');
    }
  }
  
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
          <RiskChip score={patient.riskScore} />
        </div>
        <Progress value={patient.riskScore} className="h-4" />
        <ul className="list-disc pl-6 text-muted-foreground text-lg space-y-1">
          <li>Primary drivers: {driverText || 'Analyzing patient data...'}</li>
          {protectiveFactors.length > 0 && (
            <li>Protective factor: {protectiveFactors[0]}</li>
          )}
        </ul>
        <div className="pt-2">
          <Label className="text-base uppercase tracking-wide text-muted-foreground font-semibold">Recommendations</Label>
          <div className="mt-3 grid grid-cols-1 gap-3 md:grid-cols-2">
            {recommendations.slice(0, 4).map((rec, i) => (
              <Button 
                key={i} 
                variant="secondary" 
                className="justify-start text-base py-3"
                title={rec.reason}
              >
                {rec.type === 'sleep' && <Stethoscope className="h-6 w-6 mr-2"/>}
                {rec.type === 'hrv' && <Activity className="h-6 w-6 mr-2"/>}
                {rec.type === 'activity' && <TrendingUp className="h-6 w-6 mr-2"/>}
                {rec.type === 'risk' && <ShieldAlert className="h-6 w-6 mr-2"/>}
                {rec.message}
              </Button>
            ))}
            {recommendations.length === 0 && (
              <Button variant="secondary" className="justify-start text-base py-3" disabled>
                No specific recommendations at this time
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

// Update TimelineCard to use patient data
function TimelineCard({ patient }) {
  const dot = (t) => t === "alert" ? "bg-rose-500" : t === "med" ? "bg-indigo-500" : t === "visit" ? "bg-emerald-500" : "bg-amber-500";
  const timeline = patient?.timeline || [];
  
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

// Add EHR Card component
function EHRCard({ patient }) {
  const ehr = patient?.ehr;
  if (!ehr) return null;
  
  return (
    <Card className="rounded-2xl shadow-sm">
      <CardHeader className="pb-2">
        <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><Stethoscope className="h-6 w-6" />EHR Summary</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label className="text-sm font-semibold text-muted-foreground">Diagnosis</Label>
          <p className="text-lg mt-1">{ehr.diagnosis}</p>
          <p className="text-sm text-muted-foreground">Diagnosed: {ehr.diagnosisDate ? new Date(ehr.diagnosisDate).toLocaleDateString() : 'N/A'}</p>
        </div>
        <div>
          <Label className="text-sm font-semibold text-muted-foreground">Comorbidities</Label>
          <div className="flex flex-wrap gap-2 mt-1">
            {(ehr.comorbidities || []).map((c, i) => (
              <Badge key={i} variant="outline">{c}</Badge>
            ))}
          </div>
        </div>
        <div>
          <Label className="text-sm font-semibold text-muted-foreground">Current Medications</Label>
          <div className="mt-1 space-y-2">
            {(ehr.medications || []).map((med, i) => (
              <div key={i} className="text-base">
                <strong>{med.name}</strong> {med.dose} - {med.frequency}
              </div>
            ))}
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label className="text-sm font-semibold text-muted-foreground">Blood Pressure</Label>
            <p className="text-lg mt-1">{ehr.bloodPressure || 'N/A'}</p>
          </div>
          <div>
            <Label className="text-sm font-semibold text-muted-foreground">BMI</Label>
            <p className="text-lg mt-1">{ehr.bmi || 'N/A'}</p>
          </div>
        </div>
        <div>
          <Label className="text-sm font-semibold text-muted-foreground">Clinical Notes</Label>
          <p className="text-base mt-1 text-muted-foreground">{ehr.notes || 'No notes available'}</p>
        </div>
      </CardContent>
    </Card>
  );
}

// Add Wearables Card component
function WearablesCard({ patient }) {
  const wearables = patient?.wearables;
  if (!wearables) return null;
  
  return (
    <Card className="rounded-2xl shadow-sm">
      <CardHeader className="pb-2">
        <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><Activity className="h-6 w-6" />Wearables Data</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label className="text-sm font-semibold text-muted-foreground">Device</Label>
          <p className="text-lg mt-1">{wearables.device || 'N/A'}</p>
          <p className="text-sm text-muted-foreground">Last sync: {wearables.lastSync || 'N/A'}</p>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label className="text-sm font-semibold text-muted-foreground">Avg Heart Rate</Label>
            <p className="text-lg mt-1">{wearables.heartRate?.avg || 'N/A'} bpm</p>
            <p className="text-xs text-muted-foreground">Resting: {wearables.heartRate?.resting || 'N/A'} bpm</p>
          </div>
          <div>
            <Label className="text-sm font-semibold text-muted-foreground">Steps (7d avg)</Label>
            <p className="text-lg mt-1">{(wearables.steps?.avg || 0).toLocaleString()}</p>
            <p className="text-xs text-muted-foreground">Goal: {(wearables.steps?.goal || 0).toLocaleString()}</p>
          </div>
          <div>
            <Label className="text-sm font-semibold text-muted-foreground">Sleep (7d avg)</Label>
            <p className="text-lg mt-1">{wearables.sleep?.avg || 'N/A'}h</p>
            <p className="text-xs text-muted-foreground">Quality: {wearables.sleep?.quality || 'N/A'}</p>
          </div>
          <div>
            <Label className="text-sm font-semibold text-muted-foreground">HRV (7d avg)</Label>
            <p className="text-lg mt-1">{wearables.hrv?.avg || 'N/A'} ms</p>
            <p className="text-xs text-muted-foreground">Baseline: {wearables.hrv?.baseline || 'N/A'} ms</p>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label className="text-sm font-semibold text-muted-foreground">Active Minutes</Label>
            <p className="text-lg mt-1">{wearables.activity?.activeMinutes || 'N/A'} min</p>
          </div>
          <div>
            <Label className="text-sm font-semibold text-muted-foreground">Calories</Label>
            <p className="text-lg mt-1">{wearables.activity?.calories || 'N/A'} kcal</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

// Keep existing RiskChip and Stat components
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

// Population View Component
function PopulationView() {

  const disorderBreakdown = [
    { disorder: "Depression", totalPatients: 645, highRisk: 89, networkSites: 4 },
    { disorder: "Bipolar", totalPatients: 298, highRisk: 47, networkSites: 4 },
    { disorder: "Anxiety", totalPatients: 423, highRisk: 52, networkSites: 4 },
    { disorder: "PTSD", totalPatients: 124, highRisk: 18, networkSites: 3 },
  ];

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <Card className="rounded-2xl shadow-sm lg:col-span-2">
        <CardHeader className="pb-4">
          <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><Users className="h-6 w-6"/>Network Overview</CardTitle>
        </CardHeader>
        <CardContent>
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
          <div className="grid grid-cols-2 gap-4">
            {disorderBreakdown.map((d, i) => (
              <div key={i} className="flex justify-between items-center p-5 bg-gray-50 rounded-lg">
                <div>
                  <div className="text-xl font-semibold">{d.disorder}</div>
                  <div className="text-lg text-red-600 font-semibold">{d.highRisk} high risk</div>
                </div>
                <span className="text-3xl font-bold text-indigo-600">{d.totalPatients}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
      <Card className="rounded-2xl shadow-sm">
        <CardHeader className="pb-4">
          <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><Lock className="h-6 w-6"/>Federated Learning</CardTitle>
        </CardHeader>
        <CardContent className="space-y-5">
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
        </CardContent>
      </Card>
    </div>
  );
}

export default function Component() {
  const [tab, setTab] = useState("patient");
  const [selectedPatientId, setSelectedPatientId] = useState(1);
  const [searchQuery, setSearchQuery] = useState("");
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [patientAnalytics, setPatientAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadPatients = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      console.log('[Dashboard] Loading patients...');
      const data = await apiService.getAllPatients();
      console.log('[Dashboard] Patients loaded:', data.length);
      setPatients(data);
      
      // If no patient selected yet, select first one
      if (data.length === 0) {
        setError('No patients found in database. Run the migration script to add patient data.');
      }
    } catch (err) {
      console.error('Failed to load patients:', err);
      const errorMessage = err.message.includes('Failed to fetch') || err.message.includes('NetworkError')
        ? 'Cannot connect to backend server. Make sure Flask is running on http://localhost:5000'
        : `Failed to load patients: ${err.message}`;
      setError(errorMessage);
      // Fallback to empty array
      setPatients([]);
    } finally {
      setLoading(false);
    }
  }, []);

  // Load patients on component mount
  useEffect(() => {
    loadPatients();
  }, [loadPatients]);

  // Auto-select first patient if none selected and patients are loaded
  useEffect(() => {
    if (patients.length > 0 && !selectedPatientId) {
      setSelectedPatientId(patients[0].id);
    }
  }, [patients, selectedPatientId]);

  // Load selected patient when ID changes
  useEffect(() => {
    if (selectedPatientId && patients.length > 0) {
      loadPatient(selectedPatientId);
    }
  }, [selectedPatientId, patients]);

  const loadPatient = async (id) => {
    try {
      const patient = await apiService.getPatientById(id);
      setSelectedPatient(patient);
      
      // Load patient analytics for AI insights
      try {
        const analytics = await apiService.getPatientAnalytics(id);
        setPatientAnalytics(analytics);
      } catch (analyticsErr) {
        console.warn('Failed to load patient analytics:', analyticsErr);
        // Don't fail the whole load if analytics fail
        setPatientAnalytics(null);
      }
    } catch (err) {
      console.error('Failed to load patient:', err);
      setError(`Failed to load patient ${id}`);
    }
  };

  // Filter patients based on search query
  const filteredPatients = patients.filter(p => 
    p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    p.disorder.toLowerCase().includes(searchQuery.toLowerCase()) ||
    p.disorderFull.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Calculate stats from patient data
  const avgSleep = selectedPatient?.trendData?.slice(-7).reduce((sum, d) => sum + d.sleep, 0) / 7 || 0;
  const avgHRV = selectedPatient?.trendData?.slice(-7).reduce((sum, d) => sum + d.hrv, 0) / 7 || 0;
  const avgActivity = selectedPatient?.trendData?.slice(-7).reduce((sum, d) => sum + d.activity, 0) / 7 || 0;

  // Show loading state
  if (loading && !selectedPatient) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-center">
          <div className="text-2xl font-semibold mb-2">Loading...</div>
          <div className="text-muted-foreground">Fetching patient data</div>
        </div>
      </div>
    );
  }

  // Show error state
  if (error && patients.length === 0) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-center max-w-md">
          <div className="text-2xl font-semibold mb-2 text-red-600">Error</div>
          <div className="text-muted-foreground mb-4">{error}</div>
          <Button onClick={loadPatients}>Retry</Button>
          <div className="mt-4 text-sm text-muted-foreground">
            Make sure the Flask backend is running on http://localhost:5000
          </div>
        </div>
      </div>
    );
  }

  // Show message if no patients
  if (!selectedPatient && patients.length === 0) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-center">
          <div className="text-2xl font-semibold mb-2">No patients found</div>
          <div className="text-muted-foreground">Run the migration script to populate the database</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-hidden bg-gray-50">
      {/* Sidebar */}
      <PatientSidebar
        patients={patients}
        selectedPatientId={selectedPatientId}
        onPatientSelect={setSelectedPatientId}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        filteredPatients={filteredPatients}
      />

      {/* Main Content */}
      <div className="flex-1 ml-80 overflow-y-auto">
    <div className="p-8 md:p-12 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
          <motion.div initial={{ opacity: 0, y: -6 }} animate={{ opacity: 1, y: 0 }} className="text-3xl font-semibold">
            PhenoMind Clinician Dashboard
          </motion.div>
      </div>

      <Tabs value={tab} onValueChange={setTab} className="w-full">
        <TabsList className="grid grid-cols-3 w-full md:w-auto">
          <TabsTrigger value="patient" className="text-xl py-5 font-semibold">Patient</TabsTrigger>
          <TabsTrigger value="insights" className="text-xl py-5 font-semibold">AI Insights</TabsTrigger>
          <TabsTrigger value="population" className="text-xl py-5 font-semibold">Population</TabsTrigger>
        </TabsList>

        {/* Patient tab */}
        <TabsContent value="patient" className="space-y-8 pt-6">
              {selectedPatient && <PatientHeader patient={selectedPatient} />}

          {selectedPatient && (
            <>
          {/* Top stats */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <Stat title={`${selectedPatient.disorder} Risk Level`} value={<RiskChip score={selectedPatient.riskScore} />} icon={ShieldAlert} />
            <Stat title="Avg Sleep (7d)" value={`${avgSleep.toFixed(1)} h`} delta="-0.8h" icon={CalIcon} />
            <Stat title="Heart Rate Variability (HRV) (7d)" value={`${Math.round(avgHRV)} ms`} delta="-5 ms" icon={Activity} />
            <Stat title="Activity (7d)" value={`${Math.round(avgActivity).toLocaleString()} steps`} delta="-18%" icon={TrendingUp} />
          </div>

          {/* Trends */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <TrendCard title="Mood (self-report)" dataKey="mood" data={selectedPatient.trendData || []} />
                <TrendCard title="Sleep duration" dataKey="sleep" unit=" h" data={selectedPatient.trendData || []} />
                <TrendCard title="Heart Rate Variability (HRV)" dataKey="hrv" unit=" ms" data={selectedPatient.trendData || []} />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <ForecastCard patient={selectedPatient} />
            <AISummary patient={selectedPatient} analytics={patientAnalytics} />
            <TimelineCard patient={selectedPatient} />
          </div>

          {/* EHR and Wearables */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <EHRCard patient={selectedPatient} />
            <WearablesCard patient={selectedPatient} />
          </div>
            </>
          )}
        </TabsContent>

        {/* Insights tab */}
        <TabsContent value="insights" className="space-y-8 pt-6">
          {selectedPatient && patientAnalytics ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <Card className="rounded-2xl shadow-sm lg:col-span-2">
                <CardHeader className="pb-2">
                  <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><Brain className="h-6 w-6"/>Top Biomarker Drivers</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-80">
                    {patientAnalytics.biomarkerDrivers && patientAnalytics.biomarkerDrivers.length > 0 ? (
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart 
                          data={patientAnalytics.biomarkerDrivers.map(d => {
                            // Handle both 'importance' and 'impact' field names, and 'trend' vs 'direction'
                            const importance = d.impact || d.importance || 0;
                            const trend = d.direction || d.trend || '';
                            const factor = d.factor || '';
                            const arrow = trend === 'decreasing' ? '↓' : trend === 'increasing' ? '↑' : '';
                            
                            return {
                              f: `${factor} ${arrow}`,
                              w: importance,
                              fill: importance > 0.3 ? "#dc2626" : importance > 0.2 ? "#16a34a" : importance > 0.1 ? "#8b5cf6" : "#06b6d4"
                            };
                          })} 
                          layout="vertical" 
                          margin={{ left: 10, right: 10, top: 10, bottom: 40 }}
                        >
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
                    ) : (
                      <div className="flex items-center justify-center h-full text-muted-foreground">
                        {patientAnalytics ? 'No biomarker driver data available' : 'Loading biomarker drivers...'}
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
              <Card className="rounded-2xl shadow-sm">
                <CardHeader className="pb-2">
                  <CardTitle className="text-xl font-semibold text-foreground flex items-center gap-2"><Stethoscope className="h-6 w-6"/>Treatment Recommendations</CardTitle>
                </CardHeader>
                <CardContent className="space-y-5 text-xl">
                  {patientAnalytics.recommendations && patientAnalytics.recommendations.length > 0 ? (
                    patientAnalytics.recommendations.map((rec, i) => (
                      <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-muted/50">
                        <div className="flex-1">
                          <div className="font-medium text-foreground">{rec.message}</div>
                          <div className="text-sm text-muted-foreground mt-1">{rec.reason}</div>
                        </div>
                        <Badge 
                          variant={rec.priority === 'critical' ? 'destructive' : rec.priority === 'high' ? 'default' : 'secondary'}
                          className="text-sm px-3 py-1"
                        >
                          {rec.priority}
                        </Badge>
                      </div>
                    ))
                  ) : (
                    <div className="text-muted-foreground">No specific recommendations at this time</div>
                  )}
                  <p className="text-lg text-muted-foreground mt-6">
                    {selectedPatient.disorder} relapse risk analysis for {selectedPatient.name}
                  </p>
                </CardContent>
              </Card>
            </div>
          ) : (
            <div className="flex items-center justify-center h-64 text-muted-foreground">
              {selectedPatient ? 'Loading AI insights...' : 'Select a patient to view AI insights'}
            </div>
          )}
        </TabsContent>

        {/* Population tab */}
        <TabsContent value="population" className="space-y-8 pt-6">
          <PopulationView />
        </TabsContent>
      </Tabs>
        </div>
      </div>
    </div>
  );
}