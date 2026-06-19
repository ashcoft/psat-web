import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'PSAT - Power System Analysis Toolbox',
  description: 'Web-based power system analysis and simulation tool',
};

// Using system fonts instead of Google Fonts to avoid Next.js font optimization warning
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">
        {children}
      </body>
    </html>
  );
}