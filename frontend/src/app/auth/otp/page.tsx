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
import { useForm } from "react-hook-form";
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
import { PAGES } from "@/config/pages";

const loginOTPFormSchema = z.object({
  pin: z.string().min(6).max(6),
});

export default function LoginOTP() {
  const router = useRouter();

  const form = useForm<z.infer<typeof loginOTPFormSchema>>({
    resolver: zodResolver(loginOTPFormSchema),
    defaultValues: {
      pin: "",
    },
  });

  async function onSubmit(values: z.infer<typeof loginOTPFormSchema>) {
    console.log(values);
    router.push(PAGES.DASHBOARD.HOME);
  }

  return (
    <Card className="mx-auto max-w-sm">
      <CardHeader>
        <CardTitle className="text-2xl">One-Time Password</CardTitle>
        <CardDescription>
          Enter your OTP below to login to your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <div className="grid gap-4">
              <FormField
                control={form.control}
                name="pin"
                rules={{ required: "Pflichtfeld" }}
                render={({ field }) => (
                  <FormItem className="grid gap-4">
                    <FormLabel>One-Time Password</FormLabel>
                    <FormControl>
                      <Input placeholder="XXXXXX" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button type="submit" className="w-full">
                Login
              </Button>
            </div>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
