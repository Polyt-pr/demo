export type Question = {
  id: string;
  data: string;
};

export type Poll = {
  id: string;
  question: Question;
};
