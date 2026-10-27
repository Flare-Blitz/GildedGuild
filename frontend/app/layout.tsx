import type { Metadata } from "next";
import "./globals.css";
import { Provider } from "../components/ui/provider";


export const metadata: Metadata = {
  title: "Gilded Guild",
  description: "Play the online game Gilded Guild",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
    >
      <body className="min-h-full flex flex-col">
        <Provider>
          {children}
        </Provider>
      </body>
    </html>
  );
}
