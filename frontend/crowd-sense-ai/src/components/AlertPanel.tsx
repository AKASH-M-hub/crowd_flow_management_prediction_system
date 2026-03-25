import { motion } from "framer-motion";
import { AlertTriangle, CheckCircle, Info, ChevronRight } from "lucide-react";

const alerts = [
  { id: 1, type: "critical", message: "Zone A predicted to exceed capacity in 8 mins", time: "2 min ago", icon: AlertTriangle },
  { id: 2, type: "warning", message: "Unusual crowd density detected near Gate 3", time: "5 min ago", icon: AlertTriangle },
  { id: 3, type: "info", message: "Zone B crowd levels returning to normal", time: "12 min ago", icon: Info },
  { id: 4, type: "safe", message: "All exits operating at optimal flow rate", time: "18 min ago", icon: CheckCircle },
];

const typeStyles: Record<string, { border: string; bg: string; icon: string }> = {
  critical: { border: "border-l-critical", bg: "bg-critical/5", icon: "text-critical" },
  warning: { border: "border-l-accent", bg: "bg-accent/5", icon: "text-accent" },
  info: { border: "border-l-primary", bg: "bg-primary/5", icon: "text-primary" },
  safe: { border: "border-l-safe", bg: "bg-safe/5", icon: "text-safe" },
};

const AlertPanel = () => (
  <div className="glass-card p-5">
    <div className="flex items-center justify-between mb-4">
      <h3 className="section-heading">Live Alerts</h3>
      <span className="text-[10px] bg-critical/10 text-critical px-2 py-0.5 rounded-full font-medium">
        {alerts.filter(a => a.type === "critical").length} Critical
      </span>
    </div>
    <div className="space-y-2">
      {alerts.map((alert, i) => {
        const style = typeStyles[alert.type];
        return (
          <motion.div
            key={alert.id}
            initial={{ opacity: 0, x: -12 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.08 }}
            className={`border-l-2 ${style.border} ${style.bg} rounded-r-xl p-3 flex items-center gap-3 group cursor-pointer hover:bg-secondary/40 transition-colors`}
          >
            <alert.icon className={`h-4 w-4 flex-shrink-0 ${style.icon}`} />
            <div className="flex-1 min-w-0">
              <p className="text-sm leading-snug">{alert.message}</p>
              <p className="text-[10px] text-muted-foreground mt-0.5">{alert.time}</p>
            </div>
            <ChevronRight className="h-3.5 w-3.5 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
          </motion.div>
        );
      })}
    </div>
  </div>
);

export default AlertPanel;
