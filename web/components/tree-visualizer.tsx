'use client'

import { Card } from '@/components/ui/card'
import { Animation } from '@/app/page'

interface TreeVisualizerProps {
  animation: Animation
}

export function TreeVisualizer({ animation }: TreeVisualizerProps) {
  return (
    <Card className="overflow-hidden border-0 bg-card/95 backdrop-blur-md shadow-2xl">
      <div className="relative aspect-video w-full bg-background/90">
        <iframe
          src={"https://tree-vis-v4.vercel.app/"}
          className="h-full w-full"
          style={{width: "300px", height: "300px", margin: "auto"}}
          title={`${animation.name} animation preview`}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          sandbox="allow-scripts allow-same-origin allow-presentation"
        />
      </div>
    </Card>
  );
}
