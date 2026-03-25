import { Link, useLocation } from "react-router-dom";
import { LayoutDashboard, Monitor, BarChart3, Map, Bell, Upload, Sun, Moon, User, Menu } from "lucide-react";
import { useTheme } from "@/lib/theme";
import { useState } from "react";

const navItems = [
  { label: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
  { label: "Live Monitor", path: "/dashboard", icon: Monitor },
  { label: "Analytics", path: "/dashboard", icon: BarChart3 },
  { label: "Map", path: "/dashboard", icon: Map },
  { label: "Alerts", path: "/dashboard", icon: Bell },
  { label: "Upload", path: "/dashboard", icon: Upload },
];

const Navbar = () => {
  const { pathname } = useLocation();
  const { theme, toggle } = useTheme();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 border-b border-border/30 bg-background/80 backdrop-blur-xl">
      <div className="max-w-[1600px] mx-auto px-4 md:px-6">
        <div className="flex items-center justify-between h-14">
          <Link to="/" className="flex items-center gap-2.5">
            <div className="h-8 w-8 rounded-lg bg-primary/15 border border-primary/30 flex items-center justify-center">
              <div className="h-3 w-3 rounded-sm bg-primary shadow-[0_0_8px_hsl(var(--primary)/0.5)]" />
            </div>
            <span className="text-base font-bold tracking-tight">
              Crowd<span className="text-primary">Sense</span>
            </span>
          </Link>

          <div className="hidden md:flex items-center gap-0.5 bg-secondary/50 rounded-xl p-1">
            {navItems.map(item => (
              <Link
                key={item.label}
                to={item.path}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  pathname === item.path
                    ? "bg-primary/15 text-primary shadow-sm"
                    : "text-muted-foreground hover:text-foreground hover:bg-secondary"
                }`}
              >
                <item.icon className="h-3.5 w-3.5" />
                <span className="hidden lg:inline">{item.label}</span>
              </Link>
            ))}
          </div>

          <div className="flex items-center gap-1.5">
            <button
              onClick={toggle}
              className="p-2 rounded-lg hover:bg-secondary transition-colors text-muted-foreground hover:text-foreground"
            >
              {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </button>
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="p-2 rounded-lg hover:bg-secondary transition-colors text-muted-foreground md:hidden"
            >
              <Menu className="h-4 w-4" />
            </button>
            <div className="hidden md:flex h-8 w-8 rounded-full bg-gradient-to-br from-primary/20 to-accent/20 border border-primary/20 items-center justify-center">
              <User className="h-3.5 w-3.5 text-primary" />
            </div>
          </div>
        </div>
      </div>

      {/* Mobile nav */}
      {mobileOpen && (
        <div className="md:hidden border-t border-border/30 bg-background/95 backdrop-blur-xl p-3">
          <div className="grid grid-cols-3 gap-1.5">
            {navItems.map(item => (
              <Link
                key={item.label}
                to={item.path}
                onClick={() => setMobileOpen(false)}
                className="flex flex-col items-center gap-1 p-2.5 rounded-xl text-xs text-muted-foreground hover:text-foreground hover:bg-secondary transition-all"
              >
                <item.icon className="h-4 w-4" />
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
