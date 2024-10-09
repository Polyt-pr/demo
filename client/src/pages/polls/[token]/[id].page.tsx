import type { Poll } from "@/lib/types";
import type { NextPage } from "next";
import Link from "next/link";
import { type ResponseCardProps, ResponseCard, LineMetric, StatusPill } from "@/components";
import { ChevronRight } from "lucide-react";

const Poll: NextPage = () => {
  const poll: Poll = {
    id: "1",
    question: {
      id: "1",
      data: "What is your favorite color?",
    },
  };

  const responses: ResponseCardProps[] = [
    {
      stance: "Instant communication enhances safety",
      agrees: false,
      mentions: 17,
      nuances: [
        "Smartphones facilitate quick emergency responses.",
        "Phones help students manage health emergencies.",
        "Phones facilitate planning for group activities.",
        "Phones can provide evidence against bullying.",
      ],
    },
    {
      stance: "Increased phone use harms mental health",
      agrees: true,
      mentions: 4,
      nuances: [
        "Smartphones facilitate quick emergency responses.",
        "Phones help students manage health emergencies.",
        "Phones facilitate planning for group activities.",
        "Phones can provide evidence against bullying.",
      ],
    },
  ];

  return (
    <div className="flex flex-col gap-2 max-w-[55rem] mx-auto">
      <div className="flex flex-row items-center gap-1 text-gray-500 text-sm">
        <span className="cursor-not-allowed">Dashboard</span>
        <ChevronRight size={14} />
        <Link href="/dashboard/polls" className="hover:text-black transition-colors">
          <span>Polls</span>
        </Link>
        <ChevronRight size={14} />
        <span className="font-semibold text-black">3c73a287-e150-45fa-9475-f30ffe3c66d4</span>
      </div>
      <div className="flex flex-col gap-2 mt-12">
        <StatusPill status="inactive" />
        <h1>{poll.question.data}</h1>
        <p>General overview, metrics, and analytics for a specific poll</p>
      </div>
      <div className="flex mt-4 flex-row items-center gap-8">
        <LineMetric label="Favorability" scheme={{ bg: "#FF8444", fg: "#2563EB" }} numerator={223} denominator={364} />
        <LineMetric label="Responses" numerator={234} denominator={1205} />
      </div>
      <div className="mt-4 flex flex-col gap-2">
        <label className="text-black">Reasons</label>
        <div className="flex flex-col gap-2">
          {responses.map((response, index) => (
            <ResponseCard key={index} {...response} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Poll;
