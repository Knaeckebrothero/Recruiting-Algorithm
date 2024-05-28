import { Button } from "@/components/ui/button";
import { CardDescription, CardTitle } from "@/components/ui/card";
import questions from "@/data/bip-questions";
import { ArrowUpRight, Save } from "lucide-react";
import Link from "next/link";

// Return a list of `params` to populate the [slug] dynamic segment
// export async function generateStaticParams() {
//   return questions.map((section, i) => ({
//     slug: section.id,
//   }));
// }

export default function Layout({
  params,
  children,
}: {
  params: { slug: string };
  children: React.ReactNode;
}) {
  const section = questions.find((item) => item.id === params.slug)!;

  return (
    <div>
      <div className="xl:col-span-2" x-chunk="dashboard-01-chunk-4">
        <div className="flex flex-row items-center">
          <div className="grid gap-2">
            <CardTitle>{section.header}</CardTitle>
            <CardDescription>Please answer question below</CardDescription>
          </div>
          <Button
            asChild
            size="sm"
            className="ml-auto gap-1"
            variant={"ghost"}
            disabled
          >
            <Link href="#">
              Save
              <Save className="h-4 w-4" />
            </Link>
          </Button>
        </div>
        {children}
      </div>
    </div>
  );
}
