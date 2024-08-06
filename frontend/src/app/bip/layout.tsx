import Header from "@/components/dashboard/Header";

export default function BIPLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <Header />
      <main className="min-h-screen container mt-12">{children}</main>
    </>
  );
}
