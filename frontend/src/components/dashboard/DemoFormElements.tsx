"use client";

import React from "react";
import { Input } from "../ui/input";
import { CalendarForm } from "../forms/CalendarForm";
import { RadioGroupForm } from "../forms/RadioForm";
import { SelectForm } from "../forms/SelectForm";
import { SwitchForm } from "../forms/SwitchForm";
import { Slider } from "../ui/slider";

export default function DemoFromElements() {
  return (
    <section className="flex flex-col mx-auto w-1/2 gap-5 mt-12">
      <div className="w-full">
        <span className="mb-5">Input</span>
        <Input placeholder="name.nachname" />
      </div>

      <div className="w-full">
        <CalendarForm />
      </div>
      <div className="w-full">
        <RadioGroupForm />
      </div>

      <div className="w-full">
        <SelectForm />
      </div>

      <div className="w-full">
        <SwitchForm />
      </div>

      <div className="w-full">
        <Slider defaultValue={[50]} max={100} step={25} />
      </div>
    </section>
  );
}
