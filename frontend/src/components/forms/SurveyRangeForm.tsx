"use client";
import { useScreenDetector } from "@/hooks/useScreenDetector";

import { FC, ReactNode } from "react";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { RadioGroup, RadioGroupItem } from "../ui/radio-group";
import React from "react";

export function SurveyRangeForm() {
  const { isMobile } = useScreenDetector();

  let content: ReactNode;

  if (!isMobile) {
    content = (
      <div className="flex gap-4 items-center">
        <span className="text-sm">Trift nicht zu</span>
        <RadioGroup className="flex gap-0" defaultValue="option-one">
          {[1, 2, 3, 4, 5].map((item) => {
            return (
              <div key={item} className="flex items-center">
                <Dot value={item} />
                {item !== 5 && (
                  <div className="h-0.5 bg-opacity-50 bg-gray-400 w-12"></div>
                )}
              </div>
            );
          })}
        </RadioGroup>
        <span className="text-sm">Trift voll zu</span>
      </div>
    );
  } else {
    content = (
      <Select
        onValueChange={(ev) => {
          console.log("change", ev);
        }}
      >
        <SelectTrigger>
          <SelectValue placeholder="Choose from 1 to 5" />
        </SelectTrigger>
        <SelectContent>
          <SelectGroup>
            <SelectItem value="1">1</SelectItem>
            <SelectItem value="2">2</SelectItem>
            <SelectItem value="3">3</SelectItem>
            <SelectItem value="4">4</SelectItem>
            <SelectItem value="5">5</SelectItem>
          </SelectGroup>
        </SelectContent>
      </Select>
    );
  }

  return (
    <div className="w-full flex justify-center items-center h-40">
      {content}
    </div>
  );
}

type DotProps = {
  value: number;
};

const Dot: FC<DotProps> = ({ value }) => {
  return (
    <div className="flex items-center space-x-2">
      <RadioGroupItem
        className="h-8 w-8"
        value={value.toString()}
        id={value.toString()}
      />
    </div>
  );
};
