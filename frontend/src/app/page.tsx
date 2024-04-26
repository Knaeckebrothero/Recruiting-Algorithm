"use client";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useQuery } from "@tanstack/react-query";
import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen container flex justify-center items-center">
      <Card className="mx-auto max-w-md">
        <CardHeader>
          <CardTitle className="text-2xl">Demo pages</CardTitle>
          <CardDescription>Links to Auth and Dashboard</CardDescription>
        </CardHeader>
        <CardContent>
          <Link href={"i"}>
            <Button variant={"link"}>Dashboard</Button>
          </Link>

          <Link href={"auth"}>
            <Button variant={"link"}>OTP Auth</Button>
          </Link>
        </CardContent>
      </Card>
    </main>
  );
}
