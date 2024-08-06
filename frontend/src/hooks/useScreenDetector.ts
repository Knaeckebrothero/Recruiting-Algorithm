"use client";
import { useEffect, useMemo, useState } from "react";

export const useScreenDetector = () => {
  const [width, setWidth] = useState<number | null>(null);

  const handleWindowSizeChange = () => {
    setWidth(window.innerWidth);
  };

  useEffect(() => {
    handleWindowSizeChange();
    window.addEventListener("resize", handleWindowSizeChange);

    return () => {
      window.removeEventListener("resize", handleWindowSizeChange);
    };
  }, []);

  const isMobile = useMemo(() => width && width <= 768, [width]);
  const isTablet = useMemo(() => width && width <= 1024, [width]);
  const isDesktop = useMemo(() => width && width > 1024, [width]);

  return { isMobile, isTablet, isDesktop };
};
