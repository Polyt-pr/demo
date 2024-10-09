import React from "react";
import cn from "classnames";
import { Handshake, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui";

export interface ResponseCardProps {
  stance: string;
  agrees: boolean;
  mentions: number;
  nuances: string[];
}

export const ResponseCard: React.FC<ResponseCardProps> = ({ stance, agrees, mentions, nuances }) => {
  const [isCollapsed, setIsCollapsed] = React.useState(true);

  const handleToggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div className="py-4 px-5 bg-white rounded-xl border">
      <div className="flex flex-row items-center gap-2 justify-between">
        <div className="flex flex-col">
          <h3 className="text-lg font-semibold">{stance}</h3>
          <div className="flex flex-row items-center gap-3 mt-2">
            <span
              className={cn("text-xs font-semibold", {
                "text-blue-600": agrees,
                "text-orange-600": !agrees,
              })}
            >
              {agrees ? "PRO" : "CON"}
            </span>
            <div className="flex flex-row items-center gap-1 text-sm">
              <Handshake size={15} className="text-gray-500 stroke-[2.2]" />
              <span className="font-medium text-black">{mentions} Mentions</span>
            </div>
          </div>
        </div>
        <Button onClick={handleToggleCollapse} variant="outline" className="h-10 w-10 p-0">
          <ChevronDown
            size={18}
            className={cn("text-black stroke-[2.2] transition-transform", {
              "transform rotate-180": !isCollapsed,
            })}
          />
        </Button>
      </div>
      {!isCollapsed && (
        <>
          <div className="my-6 border-t" />
          <div className="flex flex-col gap-3">
            {nuances.map((nuance, index) => (
              <p className="text-black" key={index}>
                {nuance}
              </p>
            ))}
          </div>
        </>
      )}
    </div>
  );
};
