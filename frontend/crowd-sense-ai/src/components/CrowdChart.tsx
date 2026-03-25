import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const data = [
  { time: "10:00", crowd: 120, predicted: 140 },
  { time: "10:10", crowd: 180, predicted: 200 },
  { time: "10:20", crowd: 250, predicted: 240 },
  { time: "10:30", crowd: 310, predicted: 330 },
  { time: "10:40", crowd: 280, predicted: 300 },
  { time: "10:50", crowd: 420, predicted: 400 },
  { time: "11:00", crowd: 380, predicted: 410 },
  { time: "11:10", crowd: 450, predicted: 470 },
  { time: "11:20", crowd: 520, predicted: 500 },
  { time: "11:30", crowd: 480, predicted: 540 },
];

const CrowdChart = () => (
  <div className="glass-card p-5">
    <div className="flex items-center justify-between mb-4">
      <h3 className="section-heading">Crowd Density Over Time</h3>
      <div className="flex items-center gap-4 text-[10px]">
        <span className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-primary" /> Actual
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-accent" /> Predicted
        </span>
      </div>
    </div>
    <ResponsiveContainer width="100%" height={240}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id="crowdGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="hsl(217, 91%, 60%)" stopOpacity={0.2} />
            <stop offset="100%" stopColor="hsl(217, 91%, 60%)" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="predictGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="hsl(38, 92%, 50%)" stopOpacity={0.15} />
            <stop offset="100%" stopColor="hsl(38, 92%, 50%)" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="hsl(222, 25%, 15%)" />
        <XAxis dataKey="time" stroke="hsl(217, 20%, 40%)" fontSize={11} tickLine={false} axisLine={false} />
        <YAxis stroke="hsl(217, 20%, 40%)" fontSize={11} tickLine={false} axisLine={false} />
        <Tooltip
          contentStyle={{
            backgroundColor: "hsl(222, 41%, 8%)",
            border: "1px solid hsl(222, 25%, 18%)",
            borderRadius: "12px",
            color: "hsl(210, 40%, 93%)",
            fontSize: "12px",
            boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
          }}
        />
        <Area type="monotone" dataKey="crowd" stroke="hsl(217, 91%, 60%)" fill="url(#crowdGrad)" strokeWidth={2} dot={false} />
        <Area type="monotone" dataKey="predicted" stroke="hsl(38, 92%, 50%)" fill="url(#predictGrad)" strokeWidth={1.5} strokeDasharray="4 4" dot={false} />
      </AreaChart>
    </ResponsiveContainer>
  </div>
);

export default CrowdChart;
