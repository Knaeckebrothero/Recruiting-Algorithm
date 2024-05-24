import BIPForm from "@/components/bip/bip-form";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import questions from "@/data/bip-questions";
import { ArrowUpRight } from "lucide-react";
import Link from "next/link";

// Return a list of `params` to populate the [slug] dynamic segment
export async function generateStaticParams() {
  return questions.map((section, i) => ({
    slug: section.id,
  }));
}

export default function Page({ params }: { params: { slug: string } }) {
  const section = questions.find((item) => item.id === params.slug)!;

  return (
    <div>
      <div className="xl:col-span-2" x-chunk="dashboard-01-chunk-4">
        <CardHeader className="flex flex-row items-center">
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
              <ArrowUpRight className="h-4 w-4" />
            </Link>
          </Button>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Question</TableHead>
                <TableHead className="text-right">Answer</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {section.questions.map((question) => (
                <TableRow key={question}>
                  <TableCell>
                    <div className="font-medium">{question}</div>
                    {/* <div className="hidden text-sm text-muted-foreground md:inline">
                                    liam@example.com
                                  </div> */}
                  </TableCell>
                  <TableCell className="text-right">range</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </div>
      <BIPForm />
    </div>
  );
}
