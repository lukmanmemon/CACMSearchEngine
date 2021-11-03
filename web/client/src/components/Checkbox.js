// Credit where credit is due: https://codesandbox.io/s/react-checkbox-3-xz9ol?file=/src/App.js Modified to fit use case

import './Checkbox.css'
import { useState } from "react";
import {
  animated,
  useSpring,
  config,
  useSpringRef,
  useChain
} from "react-spring";

function Checkbox({label,isChecked,setIsChecked}) {
  const checkboxAnimationRef = useSpringRef();
  const checkboxAnimationStyle = useSpring({
    backgroundColor: isChecked ? "#C4d0fb" : "#fff",
    borderColor: isChecked ? "#fff" : "#ddd",
    config: config.gentle,
    ref: checkboxAnimationRef
  });

  const [checkmarkLength, setCheckmarkLength] = useState(null);

  const checkmarkAnimationRef = useSpringRef();
  const checkmarkAnimationStyle = useSpring({
    x: isChecked ? 0 : checkmarkLength,
    config: config.gentle,
    ref: checkmarkAnimationRef
  });

  useChain(
    isChecked
      ? [checkboxAnimationRef, checkmarkAnimationRef]
      : [checkmarkAnimationRef, checkboxAnimationRef],
    [0, 0.1]
  );

  return (
    <label>
      <input
        type="checkbox"
        onChange={() => {
          setIsChecked(!isChecked);
        }}
      />
      <animated.svg
        style={checkboxAnimationStyle}
        className={`checkbox ${isChecked ? "checkbox--active" : ""}`}
        // Hide screenreader
        aria-hidden="true"
        viewBox="0 0 15 11"
        fill="none"
      >
        <animated.path
          d="M1 4.5L5 9L14 1"
          strokeWidth="2"
          stroke="#fff"
          ref={(ref) => {
            if (ref) {
              setCheckmarkLength(ref.getTotalLength());
            }
          }}
          strokeDasharray={checkmarkLength}
          strokeDashoffset={checkmarkAnimationStyle.x}
        />
      </animated.svg>
      <span>{label}</span>
    </label>
  );
}

export default Checkbox;
