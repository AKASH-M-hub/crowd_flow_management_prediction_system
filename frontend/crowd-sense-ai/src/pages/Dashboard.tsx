import { Users, TrendingUp, Gauge, Shield, Activity, Zap } from "lucide-react";
import Navbar from "@/components/Navbar";
import StatCard from "@/components/StatCard";
import LiveFeed from "@/components/LiveFeed";
import CrowdChart from "@/components/CrowdChart";
import AlertPanel from "@/components/AlertPanel";
import MapSection from "@/components/MapSection";
import ModuleLauncher from "@/components/ModuleLauncher";

const Dashboard = () => (
  <div className="min-h-screen bg-background">
    <Navbar />
    <main className="p-4 md:p-6 max-w-[1600px] mx-auto space-y-5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold tracking-tight">Command Center</h2>
          <p className="text-xs text-muted-foreground mt-0.5">Real-time crowd intelligence overview</p>
        </div>
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span className="flex items-center gap-1.5 bg-safe/10 text-safe px-2.5 py-1 rounded-full font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-safe animate-pulse" />
            System Online
          </span>
        </div>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <StatCard label="Current Crowd" value={482} icon={Users} variant="default" trend="up" />
        <StatCard label="Predicted (10m)" value={540} icon={TrendingUp} variant="warning" />
        <StatCard label="Max Capacity" value={800} icon={Gauge} />
        <StatCard label="Risk Level" value={67} suffix="%" icon={Shield} variant="warning" />
        <StatCard label="Avg Crowd" value={312} icon={Activity} />
        <StatCard label="Flow Rate" value={24} suffix="/min" icon={Zap} variant="safe" />
      </div>

      {/* Module controls */}
      <ModuleLauncher />

      {/* Main grid: Feed + Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-5">
        <div className="lg:col-span-2">
          <LiveFeed />
        </div>
        <div className="lg:col-span-3">
          <CrowdChart />
        </div>
      </div>

      {/* Alerts + Map */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <AlertPanel />
        <MapSection />
      </div>
    </main>
  </div>
);

export default Dashboard;
