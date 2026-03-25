import { motion } from "framer-motion";
import { Video, Circle, Maximize2 } from "lucide-react";

const LiveFeed = () => (
  <motion.div
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    className="glass-card p-5 h-full flex flex-col"
  >
    <div className="flex items-center justify-between mb-3">
      <h3 className="section-heading">Live Crowd Monitoring</h3>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-1.5 bg-critical/10 px-2 py-0.5 rounded-full">
          <Circle className="h-1.5 w-1.5 fill-critical text-critical animate-pulse" />
          <span className="text-[10px] text-critical font-semibold tracking-wider">LIVE</span>
        </div>
        <button className="p-1 rounded-md hover:bg-secondary transition-colors text-muted-foreground">
          <Maximize2 className="h-3.5 w-3.5" />
        </button>
      </div>
    </div>
    <div className="relative flex-1 min-h-[180px] rounded-xl bg-secondary/60 border border-border/20 overflow-hidden flex items-center justify-center">
      {/* Grid overlay */}
      <div className="absolute inset-0 opacity-[0.03]" style={{
        backgroundImage: "linear-gradient(hsl(217,91%,60%) 1px, transparent 1px), linear-gradient(90deg, hsl(217,91%,60%) 1px, transparent 1px)",
        backgroundSize: "20px 20px",
      }} />
      <div className="absolute inset-0 bg-gradient-to-t from-background/60 via-transparent to-transparent" />
      <div className="text-center z-10">
        <div className="h-16 w-16 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center mx-auto mb-3">
          <Video className="h-7 w-7 text-primary/60" />
        </div>
        <p className="text-sm font-medium text-foreground/70">Camera 01 — Main Entrance</p>
        <p className="text-xs text-muted-foreground mt-1">1920×1080 • 30fps</p>
      </div>
      {/* Scan line */}
      <div className="absolute w-full h-[1px] bg-gradient-to-r from-transparent via-primary/30 to-transparent animate-scan pointer-events-none" />
    </div>
  </motion.div>
);

export default LiveFeed;
