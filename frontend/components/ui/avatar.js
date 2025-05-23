"use client";

import * as React from "react"; import * as AvatarPrimitive from "@radix-ui/react-avatar"; import { cn } from "@/lib/utils";

const createComponent = (Component, defaultClassName = "") => React.forwardRef(({ className, ...props }, ref) => ( <Component ref={ref} className={cn(defaultClassName, className)} {...props} /> ));

const Avatar = createComponent(AvatarPrimitive.Root, "relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full"); const AvatarImage = createComponent(AvatarPrimitive.Image, "aspect-square h-full w-full"); const AvatarFallback = createComponent(AvatarPrimitive.Fallback, "flex h-full w-full items-center justify-center rounded-full bg-muted");

Avatar.displayName = AvatarPrimitive.Root.displayName; AvatarImage.displayName = AvatarPrimitive.Image.displayName; AvatarFallback.displayName = AvatarPrimitive.Fallback.displayName;

export { Avatar, AvatarImage, AvatarFallback };
