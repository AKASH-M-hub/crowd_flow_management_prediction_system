import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight, Shield, Brain, Zap, Activity } from "lucide-react";

const features = [
  { icon: Brain, title: "AI Prediction", desc: "Forecast crowd density 10 minutes ahead with deep learning models" },
  { icon: Shield, title: "Real-time Monitoring", desc: "Live CCTV analysis with computer vision and instant alerts" },
  { icon: Zap, title: "Smart Alerts", desc: "Automated warnings when capacity thresholds approach danger zones" },
];

const stats = [
  { value: "99.2%", label: "Prediction Accuracy" },
  { value: "< 2s", label: "Response Time" },
  { value: "500+", label: "Zones Monitored" },
];

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-background" />
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-primary/[0.04] rounded-full blur-[120px]" />
      <div className="absolute bottom-0 right-1/4 w-[400px] h-[400px] bg-accent/[0.03] rounded-full blur-[100px]" />
      {/* Grid pattern */}
      <div className="absolute inset-0 opacity-[0.02]" style={{
        backgroundImage: "linear-gradient(hsl(217,91%,60%) 1px, transparent 1px), linear-gradient(90deg, hsl(217,91%,60%) 1px, transparent 1px)",
        backgroundSize: "48px 48px",
      }} />

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7 }}
        className="text-center relative z-10 max-w-3xl"
      >
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="inline-flex items-center gap-2 bg-primary/10 border border-primary/20 rounded-full px-4 py-1.5 mb-8"
        >
          <Activity className="h-3.5 w-3.5 text-primary" />
          <span className="text-xs font-medium text-primary">Smart Crowd Intelligence Platform</span>
        </motion.div>

        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-5 leading-[1.1]">
          Predict Crowds
          <br />
          <span className="text-primary">Before They Happen</span>
        </h1>
        <p className="text-base md:text-lg text-muted-foreground mb-8 max-w-lg mx-auto leading-relaxed">
          AI-powered crowd intelligence that monitors, predicts, and manages crowd density in real-time for safer public spaces.
        </p>

        <div className="flex gap-3 justify-center mb-16">
          <Button
            onClick={() => navigate("/auth")}
            className="bg-primary text-primary-foreground hover:bg-primary/90 font-semibold px-6 h-11 rounded-xl"
          >
            Get Started <ArrowRight className="ml-1 h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            onClick={() => navigate("/dashboard")}
            className="border-border/60 hover:bg-secondary h-11 rounded-xl"
          >
            View Demo
          </Button>
        </div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="flex items-center justify-center gap-8 md:gap-12 mb-16"
        >
          {stats.map(s => (
            <div key={s.label} className="text-center">
              <p className="text-2xl md:text-3xl font-bold font-mono text-primary">{s.value}</p>
              <p className="text-[10px] md:text-xs text-muted-foreground mt-1 uppercase tracking-wider">{s.label}</p>
            </div>
          ))}
        </motion.div>

        {/* Feature cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {features.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 + i * 0.1 }}
              className="glass-card p-5 text-left group hover:border-primary/20 transition-all duration-500"
            >
              <div className="h-10 w-10 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center mb-3 group-hover:bg-primary/15 transition-colors">
                <f.icon className="h-5 w-5 text-primary" />
              </div>
              <h3 className="font-semibold text-sm mb-1">{f.title}</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default Index;
