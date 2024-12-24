import footerhaya from "../../assets/home/footerhaya.svg";
import lnkdin from "../../assets/home/LinkedIn.svg";
import twtr from "../../assets/home/TwitterX.svg";
import igram from "../../assets/home/Instagram.svg";
import sprinkle from "../../assets/home/sprinkle.svg";

const LINKS = [
  { href: "/#about", label: "About Haya" },
  { href: "/#how-it-works", label: "How Haya Works" },
  { href: "/#faqs", label: "FAQs" },
];

const SOCIAL_ICONS = [
  {
    href: "https://www.linkedin.com/company/hirewithhaya/",
    src: lnkdin,
    alt: "LinkedIn",
  },
  { href: "https://x.com/hirewithhaya", src: twtr, alt: "Twitter" },
  { href: "#", src: igram, alt: "Instagram" },
];

function Footer() {
  return (
    <div className="max-w-screen-2xl mx-auto pb-12 md:pb-20 px-4 md:px-8 lg:px-12">
      <div className="bg-[#F1F0FA] rounded-3xl py-4 px-4 md:px-6 lg:px-8 flex flex-col gap-16 relative overflow-hidden">
        {/* Sprinkle Background */}
        {[
          { className: "absolute select-none -top-16 left-16" },
          { className: "absolute select-none -bottom-[60%] left-[50%]" },
          { className: "absolute select-none top-0 right-0" },
        ].map((style, index) => (
          <img
            key={index}
            src={sprinkle}
            alt="sprinkle"
            className={style.className}
          />
        ))}

        {/* Top Section */}
        <div className="flex flex-wrap md:flex-nowrap justify-center gap-4 md:gap-0 md:justify-between items-center z-10">
          <a href="/">
            <img src={footerhaya} alt="Haya logo" />
          </a>
          <ul className="flex items-center gap-4 lg:gap-8">
            {LINKS.map((link, index) => (
              <li key={index}>
                <a
                  href={link.href}
                  className="font-medium text-[#1A1B21] text-sm lg:text-base"
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
          <div className="flex items-center gap-4">
            <a href="/signin">
              <button className="bg-[#E2E1EC] rounded-xl py-3 font-satoshi text-sm text-primary font-medium w-[120px]">
                Login
              </button>
            </a>
            <button className="bg-[#1A1B21] rounded-xl py-3 font-satoshi text-sm text-white font-medium w-[120px]">
              Request Access
            </button>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="flex flex-col md:flex-row gap-4 justify-between items-center z-10">
          <ul className="flex items-center gap-x-8">
            {SOCIAL_ICONS.map((icon, index) => (
              <li key={index} className="select-none">
                <a href={icon.href} target="_blank">
                  <img src={icon.src} alt={icon.alt} />
                </a>
              </li>
            ))}
          </ul>
          <p className="text-[#1A1B21] font-satoshi text-sm font-medium">
            Copyright © Haya {new Date().getFullYear()}
          </p>
          <a
            href="mailto:help@hayang.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-[#1A1B21] font-satoshi font-medium"
          >
            support: <span className="ml-1 font-semibold">help@hayang.com</span>
          </a>
        </div>
      </div>
    </div>
  );
}

export default Footer;
