import type { GetServerSideProps, NextPage } from "next";
import type { Question } from "@/lib/types";
import React from "react";
import { Button } from "@/components/ui";
import { Label, Textarea } from "@/components/ui";

type SlideStates = "intro" | "response" | "complete";

const questions: Question[] = [
  {
    id: "1",
    data: "Phones should be banned in schools.",
  },
  {
    id: "2",
    data: "The voting age should be lowered to 16.",
  },
  {
    id: "3",
    data: "The school day should be shorter.",
  },
];

interface ResponsePageProps {
  question: Question;
}

const Response: NextPage<ResponsePageProps> = ({ question }) => {
  const [currentState, setCurrentState] = React.useState<SlideStates>("intro");
  const [response, setResponse] = React.useState("");
  const [loading, setLoading] = React.useState(false);

  const handleContinue = () => {
    setCurrentState("response");
  };

  const handleResponseChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setResponse(e.target.value);
  };

  const handleSubmit = () => {
    setLoading(true);
    console.log(response);
    setLoading(false);
    setCurrentState("complete");
  };

  return (
    <div className="flex w-[calc(100vw-96px)] h-[calc(100vh-96px)] justify-center items-center">
      <div className="flex flex-col gap-2 w-[38rem] h-[15rem]">
        <h1>{currentState !== "complete" ? question.data : "Response recorded."}</h1>
        {currentState === "intro" ? (
          <>
            <p>
              Take a second to think about your position on the issue then continue to the response when you&apos;re
              ready.
            </p>
            <Button className="mt-4 w-24" onClick={handleContinue}>
              Continue
            </Button>
          </>
        ) : currentState === "response" ? (
          <div className="flex flex-col gap-2 mt-2">
            <Label htmlFor="response">What do you think?</Label>
            <Textarea
              id="response"
              placeholder="Type your message here."
              className="h-20"
              onChange={handleResponseChange}
            />
            <Button className="mt-4 w-24" disabled={!response} onClick={handleSubmit}>
              {loading ? "Loading..." : "Submit"}
            </Button>
          </div>
        ) : (
          <div className="flex flex-col gap-2">
            <p>Your response was successfully recorded. View it below and exit this page when complete.</p>
            <div className="flex flex-col gap-4 mt-4">
              <div className="flex flex-col gap-1">
                <span className="font-semibold uppercase text-xs">Question</span>
                <p>{question.data}</p>
              </div>
              <div className="flex flex-col gap-1">
                <span className="font-semibold uppercase text-xs">Response</span>
                <p>{response}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export const getServerSideProps: GetServerSideProps = async (context) => {
  const id = context.params?.id as string;

  const question = questions.find((question) => question.id === id);

  if (!question) {
    return { notFound: true };
  }

  return {
    props: { question },
  };
};

export default Response;
