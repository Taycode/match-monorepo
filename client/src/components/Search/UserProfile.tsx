import { TalentType } from "../../store/data";
import cancel from "../../assets/cancel.svg";
import document from "../../assets/document.svg";
import email from "../../assets/sms.svg";
import linkedin from "../../assets/LinkedIn.svg";
import twitter from "../../assets/TwitterX.svg";
import link from "../../assets/link-04.svg";

function UserProfile({
  isUserProfileOpen,
  talendId,
  talents,
  setIsUserProfileOpen,
}: {
  isUserProfileOpen: boolean;
  talendId: string;
  talents: TalentType[];
  setIsUserProfileOpen: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  return (
    <div
      className={`w-fit z-20 absolute left-0 right-0 md:relative md:w-3/5 ${
        !isUserProfileOpen && "hidden"
      }`}
    >
      {talents
        .filter((talent) => talent.id.toLocaleString() === talendId)
        .map((talent: TalentType) => (
          <div
            key={talent.id}
            className="border border-solid border-[#C6C5D0] bg-white w-full shadow-sm shadow-[#C6C5D0] rounded-2xl"
          >
            <div className="bg-[#05164B] h-40 w-full rounded-t-xl flex gap-3 items-center py-4 px-3 relative">
              <button
                onClick={() => setIsUserProfileOpen(false)}
                className="absolute top-3 right-3 bg-white p-1 rounded-full"
              >
                <img src={cancel} alt="cancel" className="w-4" />
              </button>
              <span className="w-16 h-16 lg:w-24 lg:h-24 rounded-full border-2 border-solid border-[#B7C4FF]">
                <img
                  src={talent.profilePicture}
                  className="md:w-fit md:h-fit rounded-full"
                />
              </span>
              <div>
                <h2 className="text-white font-medium text-lg lg:text-2xl">
                  {talent.name}
                </h2>
                <h6 className="text-white lg:text-lg lg:font-medium mt-1 font-satoshi">
                  {talent.expertise}
                </h6>
                <p className="text-white lg:text-lg lg:font-medium font-satoshi">
                  {talent.experience < 1 ? "< 1" : talent.experience} yr
                  {talent.experience > 1 ? "s" : ""} of experience
                </p>
              </div>
            </div>
            <div className="p-4 flex flex-col gap-3 w-full">
              <div className="flex items-center flex-wrap justify-between gap-2">
                <a
                  href={talent.email}
                  target="_blank"
                  className="flex items-center gap-1 py-2 px-4 bg-[#F1F0FA] rounded-lg font-satoshi text-[#05164B] text-xs lg:text-sm lg:font-medium"
                >
                  <img src={email} alt="document" />
                  Mail
                </a>
                <a
                  href={talent.twitter}
                  target="_blank"
                  className="flex items-center gap-1 py-2 px-4 bg-[#F1F0FA] rounded-lg font-satoshi text-[#05164B] text-xs lg:text-sm lg:font-medium"
                >
                  <img src={twitter} alt="" />
                  Twitter
                </a>
                <a
                  href={talent.linkedin}
                  target="_blank"
                  className="flex items-center gap-1 py-2 px-4 bg-[#F1F0FA] rounded-lg font-satoshi text-[#05164B] text-xs lg:text-sm lg:font-medium"
                >
                  <img src={linkedin} alt="" />
                  LinkedIn
                </a>
                <a
                  href={talent.website}
                  target="_blank"
                  className="flex items-center gap-1 py-2 px-4 bg-[#F1F0FA] rounded-lg font-satoshi text-[#05164B] text-xs lg:text-sm lg:font-medium"
                >
                  <img src={link} alt="" />
                  Website
                </a>
              </div>
              <a
                href={"/"}
                className="w-full bg-[#F1F0FA] rounded-xl flex items-center gap-2 p-2 text-primary font-medium font-satoshi"
              >
                <img src={document} alt="document" />
                <span>{talent.name}.pdf</span>
              </a>

              <div className="py-4 px-2 bg-[#F1F0FA] rounded-xl">
                <h2 className="text-[#1B1B1E] font-medium text-sm md:text-base">
                  Summary
                </h2>
                <hr className="w-full mt-2 mb-4 text-[#C6C5CF]" />
                <p className="text-[#2F3038] font-satoshi line-clamp-4">
                  {talent.description}
                </p>
              </div>
              <div className="py-4 px-2 bg-[#F1F0FA] rounded-xl">
                <h2 className="text-[#1B1B1E] font-medium text-sm md:text-base">
                  Skill/Stack
                </h2>
                <hr className="w-full mt-2 mb-4 text-[#C6C5CF]" />
                <div className="flex flex-col gap-2">
                  {talent.programmingLanguages && (
                    <div>
                      <h3 className="text-[#1A1B22] text-sm font-medium">
                        Programming Languages
                      </h3>
                      <p>
                        {talent.programmingLanguages.map((language) => (
                          <span
                            key={language}
                            className="mr-2 mt-1 text-[#303033] font-satoshi"
                          >
                            {language}
                          </span>
                        ))}
                      </p>
                    </div>
                  )}
                  {talent.frameworks && (
                    <div>
                      <h3 className="text-[#1A1B22] text-sm font-medium">
                        Web Frameworks
                      </h3>
                      <p>
                        {talent.frameworks.map((framework) => (
                          <span
                            key={framework}
                            className="mr-2 mt-1 text-[#303033] font-satoshi"
                          >
                            {framework}
                          </span>
                        ))}
                      </p>
                    </div>
                  )}
                  {talent.databaseManagement && (
                    <div>
                      <h3 className="text-[#1A1B22] text-sm font-medium">
                        Database Management
                      </h3>
                      <p>
                        {talent.databaseManagement.map((database) => (
                          <span
                            key={database}
                            className="mr-2 mt-1 text-[#303033] font-satoshi"
                          >
                            {database}
                          </span>
                        ))}
                      </p>
                    </div>
                  )}
                  {talent.versionControl && (
                    <div>
                      <h3 className="text-[#1A1B22] text-sm font-medium">
                        Version Control
                      </h3>
                      <p>
                        {talent.versionControl.map((ctrl) => (
                          <span
                            key={ctrl}
                            className="mr-2 mt-1 text-[#303033] font-satoshi"
                          >
                            {ctrl}
                          </span>
                        ))}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
    </div>
  );
}

export default UserProfile;
