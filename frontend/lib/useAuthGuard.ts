"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { getToken } from "./api";

/** Redirects to the sign-in screen if no token is stored. Returns the token
 * once confirmed present (null while the check is still running). */
export function useAuthGuard(): string | null {
  const router = useRouter();
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const stored = getToken();
    if (!stored) {
      router.replace("/");
      return;
    }
    setToken(stored);
  }, [router]);

  return token;
}
