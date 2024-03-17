import { html, input, DOM } from "../lib.js";
import Sortable from "sortablejs";


export function multiAutoSelect(config = {}) {
    const {
      value,
      title,
      description,
      disabled,
      autocomplete = "off",
      placeholder,
      size,
      options,
      label = "",
      list = DOM.uid("autoSelect").id,
      attr = (d) => d, // an accessor on what attribute of the object to use
      postRender = (d) => d // A function called after each element has been rendered, receives:
      // d: datum
      // button: the button used for deleting
      // ele: the html element
      // fm: the overall widget, useful for changing the return value of the widget using fm.value
      
    } = Array.isArray(config) ? { options: config } : config;
  
    const optionsMap = new Map(options.map((o) => ["" + attr(o), o])); // We need the map with strings
  
    const onAction = (fm) => {
      const addToSelected = (d) => {
        if (
          optionsMap.has(fm.input.value) && // It is an option
          fm.value.map((d) => "" + d).indexOf(fm.input.value) === -1 // If it hasn't been selected.  Need to convert to strings to do the comparison for numbers
        ) {
          fm.value.push(optionsMap.get(fm.input.value));
          renderSelection();
          fm.input.value = "";
          fm.dispatchEvent(new Event("input", { bubbles: true }));
        }
      };
      const renderSelected = (d) => {
        const button = html`<button type="button" style="margin:0px; padding:0px;">✖️</button>`;
        const ele = html`<span style="display: inline-block; margin: 7px 2px; border: solid 1px #ccc; border-radius: 5px;padding: 3px 6px; cursor:move; box-shadow: 1px 1px 1px #777; background: white">${attr(
          d
        )} ${button}</span>`;
        button.addEventListener("click", (e) => {
          fm.value.splice(fm.value.indexOf(d), 1);
          // remove the element directly
          ele.remove();
          fm.dispatchEvent(new Event("input", { bubbles: true }));
          fm.input.focus();
        });
  
        // Highlight the dragging element position
        ele.addEventListener("dragover", (e) => {
          ele.style["border-color"] = "orange";
        });
  
        // Update back to default color
        ele.addEventListener("dragleave", (e) => {
          ele.style["border-color"] = "#ccc";
        });
  
        // Update back to default color
        ele.addEventListener("dragend", (e) => {
          ele.style["border-color"] = "#ccc";
        });
  
        // Call nested selection to re-render inner elements
        postRender(d, button, ele, fm);
  
        return ele;
      };
  
      function renderSelection() {
        for (let o of fm.value) {
          //Check if the element is already selected
          if (
            ![...fm.output.childNodes]
              .map((d) => {
                // + for integer
                let data = d.firstChild?.data?.trim();
                return isNaN(+data) ? data : +data;
              })
              .includes(attr(o))
          ) {
            fm.output.appendChild(renderSelected(o));
          }
        }
  
        Sortable.create(fm.output);
        //Update event will be triggered when the user drag the selected components
        Sortable.utils.on(fm.output, "update", () => {
          fm.value = [...fm.output.childNodes].map((a) =>
            a.childNodes[0].nodeValue.trim()
          );
          fm.dispatchEvent(new Event("input", { bubbles: true }));
        });
      }
  
      fm.input.value = "";
      fm.value = value
        ? Array.isArray(value)
          ? value.filter((d) => optionsMap.has(d))
          : [value]
        : [];
      fm.onsubmit = (e) => {
        e.preventDefault();
        addToSelected();
      };
      fm.input.addEventListener("input", function (e) {
        e.stopPropagation();
        console.log("input", e);
  
        // Avoid adding the selection when still writing. Happens with numbers 🤷🏼‍♂️
        if (
          e.inputType === "insertReplacementText" ||
          e.inputType === undefined // triggered when selecting from the datalist
        ) {
          addToSelected();
        }
      });
  
  
      renderSelection();
    };
  
    const form = input({
      type: "text",
      title,
      description,
      attributes: { disabled },
      action: onAction,
      form: html`
        <form>
           ${label ? `<label>${label}</label>` : ""}
           <input name="input" type="text" autocomplete="off" 
            placeholder="${
              placeholder || ""
            }" style="font-size: 1em;" list=${list}>
            <datalist id="${list}">
                ${options.map((d) =>
                  Object.assign(html`<option>`, {
                    value: attr(d)
                  })
                )}
            </datalist>
            <br/>
        </form>
        `
    });
  
    form.output.style["margin-left"] = "0px";
    form.style["min-height"] = "2.5em";
  
    return form;
  }