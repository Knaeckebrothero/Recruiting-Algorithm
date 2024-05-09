"use client";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import z from "zod";
import { UseFormReturn, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { useRouter } from "next/navigation";

import Image from "next/image";
import Link from "next/link";

import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const signupFormSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(16),
});

export default function SignUp() {
  return (
    <div className="w-full lg:grid lg:min-h-[600px] lg:grid-cols-2 xl:min-h-[800px] h-full">
      <div className="flex items-center justify-center py-12">
        <div className="mx-auto grid w-[350px] gap-6">
          <div className="grid gap-2 text-center">
            <h1 className="text-3xl font-bold">Sign Up</h1>
            <p className="text-sm text-balance text-muted-foreground">
              Enter your information to create an account
            </p>
          </div>
          <SignUpForms />
          <div className="mt-4 text-center text-sm">
            Already have an account?{" "}
            <Link href="/auth" className="underline">
              Sign in
            </Link>
          </div>
        </div>
      </div>
      <div className="hidden bg-muted lg:block">
        <Image
          src="https://unsplash.it/800/800"
          alt="Image"
          width="1920"
          height="1080"
          className="h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
        />
      </div>
    </div>
  );
}

function SignUpForms() {
  const form = useForm<z.infer<typeof signupFormSchema>>({
    resolver: zodResolver(signupFormSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  return (
    <Tabs defaultValue="private" className="w-[400px]">
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="private">Private</TabsTrigger>
        <TabsTrigger value="business">Business</TabsTrigger>
      </TabsList>
      <TabsContent value="private">
        <PrivateAccountTab form={form} />
      </TabsContent>
      <TabsContent value="business">
        <PrivateAccountTab form={form} />
      </TabsContent>
    </Tabs>
  );
}

const PrivateAccountTab: React.FC<{
  form: UseFormReturn<z.infer<typeof signupFormSchema>>;
}> = ({ form }) => {
  async function onSubmit(values: z.infer<typeof signupFormSchema>) {
    console.log(values);
  }
  return (
    <Card>
      <CardHeader>
        <CardTitle>Private</CardTitle>
        <CardDescription>
          Enter your information to create an account
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-2">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="grid gap-4">
            <div className="grid gap-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="first-name">First name</Label>
                  <Input id="first-name" placeholder="Max" required />
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="last-name">Last name</Label>
                  <Input id="last-name" placeholder="Robinson" required />
                </div>
              </div>
            </div>
            <FormField
              control={form.control}
              name="email"
              rules={{ required: "Pflichtfeld" }}
              render={({ field }) => (
                <FormItem className="grid gap-2">
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input placeholder="m@example.com" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="password"
              rules={{ required: "Pflichtfeld" }}
              render={({ field }) => (
                <FormItem className="grid gap-2">
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input type="password" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit" className="w-full">
              Register
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};
