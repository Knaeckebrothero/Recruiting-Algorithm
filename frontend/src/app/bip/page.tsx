"use client";
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
import { ArrowUpRight } from "lucide-react";
import Link from "next/link";
import React from "react";
import sections from "@/data/bip-questions";
import { PAGES } from "@/config/pages";

export default function BIPQuestions() {
  return (
    <React.Fragment>
      <div className="w-full ">
        <Card
          className="xl:col-span-2 border-none"
          x-chunk="dashboard-01-chunk-4"
        >
          <CardHeader className="flex flex-row items-center">
            <div className="grid gap-2">
              <CardTitle>BIP Survey</CardTitle>
              <CardDescription>
                Please finish all surveys below.
              </CardDescription>
            </div>
            <Button
              asChild
              size="sm"
              className="ml-auto gap-1"
              variant={"ghost"}
              disabled
            >
              <Link href="#">
                Ergebniss
                <ArrowUpRight className="h-4 w-4" />
              </Link>
            </Button>
          </CardHeader>
          <CardContent className="border-none">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Survey</TableHead>
                  <TableHead className="text-right">Status</TableHead>
                  <TableHead className="text-right">Link</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {sections.map((section, id) => (
                  <TableRow key={section.id}>
                    <TableCell>
                      <div className="font-medium">{section.header}</div>
                      {/* <div className="hidden text-sm text-muted-foreground md:inline">
                        liam@example.com
                      </div> */}
                    </TableCell>
                    <TableCell className="text-right">
                      0 / {sections.length}
                    </TableCell>
                    <TableCell className="text-right">
                      <Button asChild variant="link">
                        <Link href={`${PAGES.BIP.HOME}/${section.id}/1`}>
                          Weiter
                        </Link>
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </React.Fragment>
  );
}
