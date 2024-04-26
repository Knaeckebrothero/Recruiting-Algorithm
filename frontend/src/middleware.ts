import { NextRequest, NextResponse } from "next/server";

export default function middleware(
  request: NextRequest,
  response: NextResponse,
) {
  const { url, cookies } = request;

  const isDashboard = url.includes("/i");
  const isAuth = url.includes("/auth");

  return NextResponse.next();
}

export const config = {
  matcher: ["/i/:path*", "/auth/:path"],
};
