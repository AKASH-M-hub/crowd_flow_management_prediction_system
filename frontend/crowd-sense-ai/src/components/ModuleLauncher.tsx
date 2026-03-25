import { useEffect, useMemo, useState } from "react";
import { Play, Square, Loader2, RefreshCw } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";
import { listModuleStates, startModule, stopModule, type ModuleKey, type ModuleState } from "@/lib/moduleApi";

const MODULE_ORDER: ModuleKey[] = ["live", "timeline", "geospatial"];

const ModuleLauncher = () => {
  const { toast } = useToast();
  const [modules, setModules] = useState<ModuleState[]>([]);
  const [loading, setLoading] = useState(true);
  const [busyModule, setBusyModule] = useState<ModuleKey | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);

  const moduleMap = useMemo(() => {
    const entries = modules.map((moduleItem) => [moduleItem.key, moduleItem] as const);
    return new Map(entries);
  }, [modules]);

  const refresh = async (silent = false) => {
    if (!silent) {
      setLoading(true);
    }
    try {
      const nextState = await listModuleStates();
      setModules(nextState);
      setApiError(null);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Could not connect to module launcher API.";
      setApiError(message);
      if (!silent) {
        toast({
          title: "Module API unavailable",
          description: message,
          variant: "destructive",
        });
      }
    } finally {
      if (!silent) {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    void refresh();

    const timer = window.setInterval(() => {
      void refresh(true);
    }, 3000);

    return () => window.clearInterval(timer);
  }, []);

  const handleStart = async (key: ModuleKey) => {
    setBusyModule(key);
    try {
      const state = await startModule(key);
      setModules((prev) => {
        const filtered = prev.filter((item) => item.key !== key);
        return [...filtered, state].sort((a, b) => MODULE_ORDER.indexOf(a.key) - MODULE_ORDER.indexOf(b.key));
      });
      toast({
        title: `${state.name} started`,
        description: `Running ${state.script}${state.pid ? ` (PID ${state.pid})` : ""}`,
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : "Could not start module.";
      toast({ title: "Start failed", description: message, variant: "destructive" });
    } finally {
      setBusyModule(null);
    }
  };

  const handleStop = async (key: ModuleKey) => {
    setBusyModule(key);
    try {
      const state = await stopModule(key);
      setModules((prev) => {
        const filtered = prev.filter((item) => item.key !== key);
        return [...filtered, state].sort((a, b) => MODULE_ORDER.indexOf(a.key) - MODULE_ORDER.indexOf(b.key));
      });
      toast({ title: `${state.name} stopped`, description: "Prediction session terminated." });
    } catch (error) {
      const message = error instanceof Error ? error.message : "Could not stop module.";
      toast({ title: "Stop failed", description: message, variant: "destructive" });
    } finally {
      setBusyModule(null);
    }
  };

  return (
    <Card>
      <CardHeader className="flex flex-row items-start justify-between gap-4">
        <div>
          <CardTitle className="text-base">Execution Modules</CardTitle>
          <CardDescription>
            Launch Python modules from frontend: main.py, main2.py, and geospatial_dashboard.py.
          </CardDescription>
        </div>
        <Button variant="outline" size="sm" onClick={() => void refresh()} disabled={loading || busyModule !== null}>
          <RefreshCw className="h-4 w-4 mr-1.5" />
          Refresh
        </Button>
      </CardHeader>
      <CardContent className="space-y-3">
        {apiError && (
          <div className="rounded-md border border-destructive/40 bg-destructive/10 p-3 text-xs text-destructive">
            API connection error: {apiError}. Start backend with: python frontend/module_launcher_api.py
          </div>
        )}

        {MODULE_ORDER.map((key) => {
          const moduleItem = moduleMap.get(key);
          const isBusy = busyModule === key;
          const isRunning = moduleItem?.status === "running";

          return (
            <div key={key} className="rounded-lg border border-border/70 p-3 md:p-4">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2">
                    <p className="text-sm font-semibold">{moduleItem?.name ?? key}</p>
                    <Badge variant={isRunning ? "default" : "secondary"}>
                      {isRunning ? "Running" : "Stopped"}
                    </Badge>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">{moduleItem?.description}</p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Script: <span className="font-medium">{moduleItem?.script ?? "-"}</span>
                    {isRunning && moduleItem?.pid ? ` | PID: ${moduleItem.pid}` : ""}
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <Button
                    size="sm"
                    onClick={() => void handleStart(key)}
                    disabled={isBusy || loading || isRunning}
                    className="min-w-24"
                  >
                    {isBusy ? <Loader2 className="h-4 w-4 mr-1.5 animate-spin" /> : <Play className="h-4 w-4 mr-1.5" />}
                    Start
                  </Button>
                  <Button
                    size="sm"
                    variant="destructive"
                    onClick={() => void handleStop(key)}
                    disabled={isBusy || loading || !isRunning}
                    className="min-w-24"
                  >
                    {isBusy ? <Loader2 className="h-4 w-4 mr-1.5 animate-spin" /> : <Square className="h-4 w-4 mr-1.5" />}
                    Stop
                  </Button>
                </div>
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
};

export default ModuleLauncher;
