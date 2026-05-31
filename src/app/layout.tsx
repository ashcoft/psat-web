import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'PSAT - Power System Analysis Toolbox',
  description: 'Web-based power system analysis and simulation tool',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className="font-sans antialiased">
        {children}
      </body>
    </html>
  );
}