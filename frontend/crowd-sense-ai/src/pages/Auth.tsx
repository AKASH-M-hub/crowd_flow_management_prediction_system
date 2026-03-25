import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowRight, Activity } from "lucide-react";

const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      <div className="absolute inset-0 bg-background" />
      <div className="absolute top-1/3 left-1/3 w-[500px] h-[500px] bg-primary/[0.03] rounded-full blur-[120px]" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="glass-card p-8 w-full max-w-sm relative z-10"
      >
        <div className="text-center mb-7">
          <div className="h-12 w-12 rounded-xl bg-primary/15 border border-primary/25 flex items-center justify-center mx-auto mb-4">
            <Activity className="h-6 w-6 text-primary" />
          </div>
          <h1 className="text-xl font-bold tracking-tight">
            Crowd<span className="text-primary">Sense</span> AI
          </h1>
          <p className="text-xs text-muted-foreground mt-1.5">
            {isLogin ? "Welcome back" : "Create your account"}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          {!isLogin && (
            <Input placeholder="Full Name" className="bg-secondary/60 border-border/40 h-10 rounded-xl text-sm" />
          )}
          <Input type="email" placeholder="Email" className="bg-secondary/60 border-border/40 h-10 rounded-xl text-sm" />
          <Input type="password" placeholder="Password" className="bg-secondary/60 border-border/40 h-10 rounded-xl text-sm" />

          <Button type="submit" className="w-full bg-primary text-primary-foreground hover:bg-primary/90 font-semibold h-10 rounded-xl">
            {isLogin ? "Login" : "Create Account"} <ArrowRight className="ml-1 h-4 w-4" />
          </Button>
        </form>

        <p className="text-center text-xs text-muted-foreground mt-5">
          {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
          <button onClick={() => setIsLogin(!isLogin)} className="text-primary hover:underline font-medium">
            {isLogin ? "Sign Up" : "Login"}
          </button>
        </p>
      </motion.div>
    </div>
  );
};

export default Auth;
