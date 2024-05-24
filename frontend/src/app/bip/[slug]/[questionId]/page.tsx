"use client";
import { SurveyRangeForm } from "@/components/forms/SurveyRangeForm";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import questions from "@/data/bip-questions";
import Link from "next/link";

// Return a list of `params` to populate the [slug] dynamic segment
// export async function generateStaticParams() {
//   const pages = questions
//     .map((section) => {
//       return section.questions.map((item, i) => {
//         return {
//           slug: section.id,
//           questionId: i.toString(),
//         };
//       });
//     })
//     .flat();

//   return pages;
// }

export default function Page({
  params,
}: {
  params: { slug: string; questionId: string };
}) {
  const section = questions.find((item) => item.id === params.slug)!;
  const question = section.questions.find(
    (item, i) => i + 1 === Number(params.questionId),
  )!;

  return (
    <Card className="mt-10">
      <CardHeader>
        <CardTitle>Question {params.questionId} / 10:</CardTitle>
      </CardHeader>

      <CardContent>
        <h2 className=" mt-4 text-xl font-semibold">{question}</h2>
        <SurveyRangeForm />
        <div className="grid grid-cols-2">
          {Number(params.questionId) !== 1 && (
            <Button
              size="sm"
              className="justify-self-start col-start-1"
              variant="default"
              asChild
            >
              <Link
                href={`/bip/${params.slug}/${Number(params.questionId) - 1}`}
              >
                Previous
              </Link>
            </Button>
          )}
          {Number(params.questionId) !== section.questions.length && (
            <Button
              size="sm"
              className="justify-self-end col-start-2"
              variant="default"
              asChild
            >
              <Link
                href={`/bip/${params.slug}/${Number(params.questionId) + 1}`}
              >
                Next
              </Link>
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
