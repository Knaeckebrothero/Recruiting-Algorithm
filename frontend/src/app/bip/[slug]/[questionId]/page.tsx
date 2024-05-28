"use client";
import { SurveyRangeForm } from "@/components/forms/SurveyRangeForm";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Form } from "@/components/ui/form";

import questions from "@/data/bip-questions";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";

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
    (_item, i) => i + 1 === Number(params.questionId),
  )!;

  const form = useForm();
  const router = useRouter();

  const onSubmit = (data: any) => {
    console.log(data);

    if (section.questions.length !== Number(params.questionId)) {
      router.push(`/bip/${params.slug}/${Number(params.questionId) + 1}`);
    } else {
      router.push(`/bip/`);
    }
  };

  return (
    <Card className="mt-10">
      <CardHeader>
        <CardTitle>Question {params.questionId} / 10:</CardTitle>
      </CardHeader>

      <CardContent>
        <h2 className=" mt-4 text-xl font-semibold">{question}</h2>
        <Form {...form}>
          <SurveyRangeForm form={form} />
          <form
            className="grid grid-cols-2"
            onSubmit={form.handleSubmit(onSubmit)}
          >
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
            <Button
              size="sm"
              className="justify-self-end col-start-2"
              variant="default"
              type="submit"
              disabled={!form.formState.isValid}
            >
              {section.questions.length === Number(params.questionId)
                ? "Finish"
                : "Next"}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
