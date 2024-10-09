import type { Poll } from "@/lib/types";
import type { NextPage } from "next";
import { PollPreviewCard } from "@/components";
import { ChevronRight } from "lucide-react";

const Polls: NextPage = () => {
  const polls: Poll[] = [
    {
      id: "1",
      question: {
        id: "1",
        data: "What is your favorite color?",
      },
    },
    {
      id: "2",
      question: {
        id: "2",
        data: "What is your favorite animal?",
      },
    },
    {
      id: "3",
      question: {
        id: "3",
        data: "What is your favorite food?",
      },
    },
  ];

  return (
    <div className="flex flex-col gap-2 max-w-[55rem] mx-auto">
      <div className="flex flex-row items-center gap-1 text-gray-500 text-sm">
        <span className="cursor-not-allowed">Dashboard</span>
        <ChevronRight size={14} />
        <span className="font-semibold text-black">Polls</span>
      </div>
      <div className="flex flex-col gap-2 mt-12">
        <h1>Your Polls</h1>
        <p>A collection of all your organizations polls.</p>
      </div>
      <div className="mt-4 flex flex-col gap-4">
        {polls.map((poll) => (
          <PollPreviewCard key={poll.id} {...poll} />
        ))}
      </div>
    </div>
  );
};

export default Polls;
