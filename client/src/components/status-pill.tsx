import React from "react";
import cn from "classnames";

interface StatusPillProps {
  status: "active" | "inactive";
}

export const StatusPill: React.FC<StatusPillProps> = ({ status }) => {
  return (
    <div
      className={cn("w-fit px-2 py-1 text-xs font-semibold rounded-full", {
        "bg-green-200 text-green-800": status === "active",
        "bg-orange-100 text-orange-600": status === "inactive",
      })}
    >
      {status === "active" ? "Active" : "Inactive"}
    </div>
  );
};
