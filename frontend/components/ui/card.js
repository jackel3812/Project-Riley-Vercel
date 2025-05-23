"use client";

import * as React from "react"; import { cn } from "@/lib/utils";

const createComponent = (displayName, defaultClassName) => { const Component = React.forwardRef(({ className, ...props }, ref) => ( <div ref={ref} className={cn(defaultClassName, className)} {...props} /> )); Component.displayName = displayName; return Component; };

const Card = createComponent("Card", "rounded-lg border bg-card text-card-foreground shadow-sm"); const CardHeader = createComponent("CardHeader", "flex flex-col space-y-1.5 p-6"); const CardContent = createComponent("CardContent", "p-6 pt-0"); const CardFooter = createComponent("CardFooter", "flex items-center p-6 pt-0");

const CardTitle = React.forwardRef(({ className, ...props }, ref) => ( <h3 ref={ref} className={cn("text-2xl font-semibold leading-none tracking-tight", className)} {...props} /> )); CardTitle.displayName = "CardTitle";

const CardDescription = React.forwardRef(({ className, ...props }, ref) => ( <p ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} /> )); CardDescription.displayName = "CardDescription";

export { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter };
