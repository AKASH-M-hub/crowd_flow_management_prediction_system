import { motion } from "framer-motion";
import { MapPin, Crosshair } from "lucide-react";

const zones = [
  { id: 1, name: "Zone A", x: "22%", y: "28%", status: "critical", count: 520 },
  { id: 2, name: "Zone B", x: "58%", y: "42%", status: "safe", count: 180 },
  { id: 3, name: "Zone C", x: "38%", y: "68%", status: "warning", count: 340 },
  { id: 4, name: "Zone D", x: "72%", y: "22%", status: "safe", count: 95 },
  { id: 5, name: "Zone E", x: "80%", y: "65%", status: "warning", count: 270 },
];

const dotStyles: Record<string, string> = {
  critical: "bg-critical shadow-[0_0_12px_hsl(var(--critical)/0.6)]",
  warning: "bg-accent shadow-[0_0_12px_hsl(var(--warning)/0.5)]",
  safe: "bg-safe shadow-[0_0_12px_hsl(var(--safe)/0.5)]",
};

const ringStyles: Record<string, string> = {
  critical: "border-critical/30",
  warning: "border-accent/30",
  safe: "border-safe/30",
};

const MapSection = () => (
  <div className="glass-card p-5">
    <div className="flex items-center justify-between mb-4">
      <h3 className="section-heading">
        <Crosshair className="inline h-3.5 w-3.5 mr-1.5 -mt-0.5" />
        Area Capacity Analysis
      </h3>
      <span className="text-[10px] text-muted-foreground">
        {zones.length} zones monitored
      </span>
    </div>
    <div className="relative w-full h-56 md:h-64 rounded-xl bg-secondary/40 border border-border/20 overflow-hidden">
      {/* Grid overlay */}
      <div className="absolute inset-0 opacity-[0.04]" style={{
        backgroundImage: "linear-gradient(hsl(217,91%,60%) 1px, transparent 1px), linear-gradient(90deg, hsl(217,91%,60%) 1px, transparent 1px)",
        backgroundSize: "32px 32px",
      }} />
      {/* Radial overlay */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_30%,hsl(222,47%,5%,0.6))]" />

      {zones.map((zone, i) => (
        <motion.div
          key={zone.id}
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.1 + i * 0.08 }}
          className="absolute group cursor-pointer"
          style={{ left: zone.x, top: zone.y }}
        >
          <div className={`w-5 h-5 rounded-full border-2 ${ringStyles[zone.status]} flex items-center justify-center animate-pulse-glow`}>
            <div className={`w-2.5 h-2.5 rounded-full ${dotStyles[zone.status]}`} />
          </div>
          <div className="absolute bottom-7 left-1/2 -translate-x-1/2 bg-card/90 backdrop-blur-xl border border-border/50 px-3 py-2 rounded-xl opacity-0 group-hover:opacity-100 transition-all duration-200 whitespace-nowrap shadow-xl scale-95 group-hover:scale-100">
            <p className="text-xs font-semibold">{zone.name}</p>
            <p className="text-[10px] text-muted-foreground">{zone.count} people</p>
          </div>
        </motion.div>
      ))}
    </div>
  </div>
);

export default MapSection;
