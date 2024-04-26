export default function AuthLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <main className="min-h-screen container flex justify-center items-center">
      {children}
    </main>
  );
}
