import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'GraphMind AI - Engineering Cognition Platform',
  description: 'AI-Native Engineering Cognition Platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

// Made with Bob
