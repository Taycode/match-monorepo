import back from "../../assets/back.svg";
import like from "../../assets/like.svg";
import { TalentType } from "../../store/data";

function UserCard({
  talent,
  isUserProfileOpen,
  setIsUserProfileOpen,
  setTalentId,
}: {
  talent: TalentType;
  isUserProfileOpen: boolean;
  setIsUserProfileOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setTalentId: React.Dispatch<React.SetStateAction<string>>;
}) {
  return (
    <div className="flex items-center justify-between w-full bg-[#F1F0FA] rounded-xl px-4 py-2">
      <div className="flex gap-3 items-center max-w-[150px] md:max-w-[200px] lg:max-w-sm w-full">
        <span className="w-20 h-20 hidden lg:block border border-solid border-primary rounded-full">
          <img
            src={talent.profilePicture}
            alt={talent.name}
            className="w-fit h-fit rounded-full"
          />
        </span>

        <div>
          <h2 className="text-[#1A1B22] font-medium text-sm md:text-lg lg:text-xl max-w-[150px] md:max-w-[200px] lg:max-w-sm overflow-hidden truncate">
            {talent.name}
          </h2>
          <h6 className="text-[#5E5E62] text-xs md:text-base font-medium mt-1 font-satoshi">
            {talent.expertise}
          </h6>
          <p className="text-[#5E5E62] text-xs md:text-base font-medium mt-1 font-satoshi">
            {talent.experience < 1 ? "< 1" : talent.experience} yr
            {talent.experience > 1 ? "s" : ""} of experience
          </p>
        </div>
      </div>

      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-center gap-1 bg-secondary p-2 rounded-lg">
          <img src={like} alt="like" />
          <span className="text-white font-bold text-xs">{talent.score}</span>
        </div>
        <h4 className="text-secondary font-bold text-[11px]">Match Score</h4>
      </div>

      <button
        onClick={() => {
          setIsUserProfileOpen(true);
          setTalentId(talent.id.toLocaleString());
        }}
        className="flex items-center gap-2 bg-transparent"
      >
        <span
          className={`text-primary font-medium font-satoshi hidden md:block ${
            isUserProfileOpen && "hidden"
          }`}
        >
          View Profile
        </span>
        <img src={back} alt="back" className="rotate-180" />
      </button>
    </div>
  );
}

export default UserCard;
