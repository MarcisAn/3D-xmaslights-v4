"use client";

import { Card } from "@/components/ui/card";
import { Animation } from "@/app/page";
import { Check } from "lucide-react";
import { cn } from "@/lib/utils";

interface AnimationListProps {
  animations: Animation[];
  selectedAnimation: Animation;
  onSelectAnimation: (animation: Animation) => void;
}

export function AnimationList({
  animations,
  selectedAnimation,
  onSelectAnimation,
}: AnimationListProps) {
  
  function selectAnim(animation: Animation) {
    // onSelectAnimation(animation);
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    
    const raw = JSON.stringify({
      name: animation.name,
    });

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: raw,
      redirect: "follow",
    };

    fetch("https://ledserver.andersons-m.lv/pickAnim", requestOptions)
      .then((response) => response.text())
      .then((result) => console.log(result))
      .catch((error) => console.error(error));
  }
  
  
  return (
    <Card className="flex flex-col border-0 bg-card/95 backdrop-blur-md shadow-2xl">
      <div className="bg-primary/30 px-6 py-4 border-b-[6px] border-primary">
        <h2 className="font-bold text-xl text-foreground">Pieejamās animācijas</h2>
      </div>
      <div className="flex-1 space-y-3 p-6">
        {animations.map((animation) => {
          const isSelected = selectedAnimation.name === animation.name;
          return (
            <button
              key={animation.name}
              onClick={() => selectAnim(animation)}
              className={cn(
                "group relative w-full border-l-[6px] bg-muted/80 p-4 text-left transition-all hover:bg-secondary/30 hover:border-secondary hover:shadow-lg border-transparent"
              )}>
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1">
                  <h3 className="font-bold text-foreground">
                    {animation.full_name}
                  </h3>
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </Card>
  );
}
