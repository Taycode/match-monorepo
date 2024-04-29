import { useState } from "react";
import faqCard from "../../assets/home/faqcard.svg";
import { PlusIcon, MinusIcon } from "../../assets/icons";

const faqData: {
  question: string;
  content: string;
}[] = [
  {
    question: "What sets Haya apart from traditional hiring methods?",
    content:
      "Unlike traditional hiring methods, Haya offers precision matching tailored to companies' unique needs. It simplifies the hiring process, saves time, and ensures a higher likelihood of finding the right fit for both parties.",
  },
  {
    question: "How can tech professionals benefit from Haya?",
    content:
      "Tech professionals can leverage on Haya to explore diverse job oppurtunies that align with their skills, passions, and career goals. By creating profiles showcasing their expertise, they can connect with companies actively seeking their talents.",
  },
  {
    question: "What industries does Haya serve?",
    content:
      "Haya serves a wide range of industries, including but not limited to technology, finance, healthcare, e-commerce, gaming and more. We cater to businesses of all sizes, from startups to enterprises, across various sectors.",
  },
  {
    question: "How does Haya ensure privacy and data security?",
    content:
      "We prioritize the privacy and data security of both businesses and tech professionals on Haya. We implement robust encryption measures, adhere to strict data protection regulations, and ensure confidentiality throughout the hiring process.",
  },
  {
    question: "Is there a fee for using Haya?",
    content:
      "Signing up and creating profiles on Haya is free for both businesses and tech professionals. However, there may be fees associated with premium features or additional services, which we offer at competitive rates.",
  },
];

function Faq() {
  const [isOpen, setIsOpen] = useState(null);
  const toggleOpen = (id: any) => () =>
    setIsOpen((isOpen) => (isOpen === id ? null : id));

  return (
    <div
      className="max-w-screen-2xl mx-auto px-12 py-20 flex justify-between gap-24"
      id="faqs"
    >
      <div className="min-w-3/5 grow flex flex-col">
        {faqData.map(({ content, question }, index) => (
          <Question
            key={index}
            content={content}
            question={question}
            isOpen={isOpen === index}
            toggle={toggleOpen(index)}
          />
        ))}
      </div>
      <img src={faqCard} alt="faq card" className="hidden md:block" />
    </div>
  );
}

export default Faq;

function Question({ toggle, question, content, isOpen }: any) {
  return (
    <div
      onClick={toggle}
      className="cursor-pointer px-6 md:px-8 py-3 md:py-6 border-0 border-b-2 border-solid border-[#E2E1EC] hover:border-secondary"
    >
      <div className="flex items-center justify-between">
        <h2 className="text-sm md:text-lg font-medium md:lg max-w-[250px] md:max-w-full">
          {question}
        </h2>
        {isOpen ? <MinusIcon className="w-5" /> : <PlusIcon className="w-5" />}
      </div>
      {isOpen && (
        <p className="mt-4 text-sm md:text-base font-normal font-satoshi">
          {content}
        </p>
      )}
    </div>
  );
}
