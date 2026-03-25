import { useEffect, useState } from "react";

const AnimatedCounter = ({ value, duration = 1000 }: { value: number; duration?: number }) => {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    let start = 0;
    const step = value / (duration / 16);
    const timer = setInterval(() => {
      start += step;
      if (start >= value) { setDisplay(value); clearInterval(timer); }
      else setDisplay(Math.floor(start));
    }, 16);
    return () => clearInterval(timer);
  }, [value, duration]);

  return <span className="animate-count-up">{display.toLocaleString()}</span>;
};

export default AnimatedCounter;
