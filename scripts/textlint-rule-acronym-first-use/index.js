"use strict";

const DEFAULT_MIN_LENGTH = 3;
const DEFAULT_MAX_LENGTH = 5;

function isPlausibleExpansion(text) {
    const words = text.trim().split(/\s+/).filter((word) => /[A-Za-z]/.test(word));
    return words.length >= 2 && /[a-z]/.test(text);
}

module.exports = function acronymFirstUse(context, options = {}) {
    const { Syntax, getSource, locator, report, RuleError } = context;
    const minLength = Number.isInteger(options.min_acronym_len)
        ? Math.max(2, options.min_acronym_len)
        : DEFAULT_MIN_LENGTH;
    const maxLength = Number.isInteger(options.max_acronym_len)
        ? Math.max(minLength, options.max_acronym_len)
        : DEFAULT_MAX_LENGTH;
    const ignored = new Set(options.ignore_acronyms || []);
    const seen = new Set();
    const acronymPattern = new RegExp(
        `\\b([A-Z][A-Z0-9]{${minLength - 1},${maxLength - 1}})(?:s)?\\b`,
        "g"
    );

    return {
        [Syntax.Document]() {
            seen.clear();
        },

        [Syntax.Str](node) {
            const text = getSource(node);

            for (const match of text.matchAll(acronymPattern)) {
                const acronym = match[1];
                if (ignored.has(acronym) || seen.has(acronym)) {
                    continue;
                }

                seen.add(acronym);
                const remainder = text.slice(match.index + match[0].length);
                const expansion = remainder.match(/^\s+\(([^()\n]+)\)/);
                if (expansion && isPlausibleExpansion(expansion[1])) {
                    continue;
                }

                report(
                    node,
                    new RuleError(
                        `Expand ${acronym} on first use by following it with ` +
                            "its full term in parentheses.",
                        {
                            padding: locator.range([
                                match.index,
                                match.index + match[0].length,
                            ]),
                        }
                    )
                );
            }
        },
    };
};
