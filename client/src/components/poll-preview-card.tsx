import type { Poll } from "@/lib/types";
import React from "react";
import Link from "next/link";
import { MessageCircleReply, HeartHandshake } from "lucide-react";
import { Button } from "@/components/ui";
import { StatusPill } from "@/components";

type PollPreviewCardProps = Poll & {};

export const PollPreviewCard: React.FC<PollPreviewCardProps> = ({ id, question }) => {
  return (
    <div className="p-4 bg-white rounded-xl border">
      <h3 className="text-lg font-semibold">{question.data}</h3>
      <div className="flex flex-row items-center gap-3 mt-2">
        <StatusPill status="inactive" />
        <div className="flex flex-row items-center gap-1 text-sm">
          <MessageCircleReply size={15} className="text-gray-500 stroke-[2.2]" />
          <span className="font-medium">17/22</span>
        </div>
        <div className="flex flex-row items-center gap-1 text-sm">
          <HeartHandshake size={15} className="text-gray-500 stroke-[2.2]" />
          <span className="font-medium">5</span>
        </div>
      </div>
      <Link href={`/dashboard/polls/${id}`}>
        <Button variant="outline" className="mt-6">
          View Poll
        </Button>
      </Link>
    </div>
  );
};
