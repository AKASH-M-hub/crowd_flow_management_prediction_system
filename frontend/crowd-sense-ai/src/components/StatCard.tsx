import { motion } from "framer-motion";
import { LucideIcon, TrendingUp, TrendingDown } from "lucide-react";
import AnimatedCounter from "./AnimatedCounter";

interface StatCardProps {
  label: string;
  value: number;
  icon: LucideIcon;
  suffix?: string;
  trend?: "up" | "down";
  variant?: "default" | "warning" | "safe" | "critical";
}

const variantStyles = {
  default: { text: "text-primary", bg: "bg-primary/8", dot: "bg-primary" },
  warning: { text: "text-accent", bg: "bg-accent/8", dot: "bg-accent" },
  safe: { text: "text-safe", bg: "bg-safe/8", dot: "bg-safe" },
  critical: { text: "text-critical", bg: "bg-critical/8", dot: "bg-critical" },
};

const StatCard = ({ label, value, icon: Icon, suffix = "", trend, variant = "default" }: StatCardProps) => {
  const styles = variantStyles[variant];
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card p-4 group hover:glass-card-elevated transition-all duration-500 hover:border-primary/20"
    >
      <div className="flex items-center justify-between mb-3">
        <span className="section-heading">{label}</span>
        <div className={`p-1.5 rounded-lg ${styles.bg}`}>
          <Icon className={`h-3.5 w-3.5 ${styles.text}`} />
        </div>
      </div>
      <div className={`stat-value ${styles.text} mb-1`}>
        <AnimatedCounter value={value} />
        <span className="text-lg ml-0.5">{suffix}</span>
      </div>
      {trend && (
        <div className={`flex items-center gap-1 text-xs mt-2 ${trend === "up" ? "text-accent" : "text-safe"}`}>
          {trend === "up" ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
          <span>{trend === "up" ? "Increasing" : "Decreasing"}</span>
        </div>
      )}
    </motion.div>
  );
};

export default StatCard;
