import React from "react";

type ColorScheme = {
  bg: string;
  fg: string;
};

interface LineMetricProps {
  label: string;
  numerator: number;
  denominator: number;
  scheme?: ColorScheme;
}

export const LineMetric: React.FC<LineMetricProps> = ({
  label,
  numerator,
  denominator,
  scheme = { bg: "#DADADA", fg: "#000000" },
}) => {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-black">{label}</label>
      <div className="relative w-40 rounded-2xl overflow-hidden h-3">
        <div style={{ backgroundColor: scheme.bg }} className="absolute w-full bg-blue-200 h-full rounded-2xl" />
        <div
          style={{ width: `${(numerator / denominator) * 100}%`, backgroundColor: scheme.fg }}
          className="z-10 absolute left-0 bg-red-500 h-full rounded-2xl"
        />
      </div>
      <div className="flex flex-row items-center justify-between">
        <span className="text-gray-500 text-xs">
          {numerator} / {denominator}
        </span>
        <span className="text-gray-500 text-xs">{Math.round((numerator / denominator) * 100)}%</span>
      </div>
    </div>
  );
};
