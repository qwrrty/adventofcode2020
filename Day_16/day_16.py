#! /usr/bin/env python3

from collections import defaultdict


def get_puzzle_input(filename="input.txt"):
    with open(filename, "r") as f:
        text = f.read()
    return text


class TicketValidator(object):

    def __init__(self, rules):
        self.rules = defaultdict(list)
        
        for rule in rules.split("\n"):
            if not rule:
                continue
            rule_name, rule_text = rule.split(": ")
            for range_str in rule_text.split(" or "):
                lo, hi = range_str.split("-")
                self.rules[rule_name].append(range(int(lo), int(hi)+1))

    def valid_fields(self, val, candidates):
        # Return a list of field names from "candidates"
        # for which val could be a plausible match.
        fields = []
        for rule in candidates:
            ranges = self.rules[rule]
            for r in ranges:
                if val in r:
                    fields.append(rule)
                    break
        return fields

    def is_valid_field(self, val):
        return self.valid_fields(val, candidates=self.rules.keys())

    def scanning_error_rate(self, ticket):
        vals = [int(x) for x in ticket.split(",")]
        error_rate = []
        for v in vals:
            if not self.is_valid_field(v):
                error_rate.append(v)
        return error_rate

    # Take a list of "nearby tickets" and identify which columns must
    # correspond to which ticket fields.
    #
    # We will maintain a list of candidate ticket fields for each
    # column in the written ticket.
    #
    # 1. This list will be initialized to have all possible candidates
    #    in each column.
    #
    # 2. Iterate through the list of tickets. For each column, eliminate
    #    any candidate fields that are contraindicated by one or more
    #    ticket columns.
    #
    # 3. Repeatedly cycle through the list of candidate fields. For each
    #    column that has been narrowed down to one possible field, eliminate
    #    that column from the other candidates.
    #
    # 4. Repeat step 3 until all columns have been assigned to exactly
    #    one field.

    def identify_ticket_fields(self, nearby_tickets):
        # Initialize a list of candidate fields
        # Each index of the candidates list holds a set of possible fields.
        candidates = [set(self.rules.keys())
                      for x in range(len(self.rules.keys()))]

        # Make a first pass at eliminating candidates based on
        # ticket column values.
        for ticket in nearby_tickets:
            if not ticket:
                continue
            # First, eliminate invalid tickets entirely.
            if self.scanning_error_rate(ticket):
                continue
            # Iterate through each ticket column and figure out
            # which fields can be eliminated.
            columns = ticket.split(",")
            for i, column in enumerate(columns):
                val = int(column)
                winnowed_fields = self.valid_fields(val, candidates[i])
                candidates[i] = set(winnowed_fields)

        # Iterate through the list of candidates. For each column that has
        # been narrowed down to one field, eliminate it from the rest of
        # the candidates.
        done = False
        while not done:
            done = True
            for field_set in candidates:
                if len(field_set) == 1:
                    # We've narrowed this field down to one candidate.
                    # Remove this field from all other column candidate pools.
                    field = list(field_set)[0]
                    for i in range(len(candidates)):
                        if len(candidates[i]) > 1 and field in candidates[i]:
                            candidates[i].remove(field)
                else:
                    done = False

        # Return a map that says which candidate maps to which column
        field_map = {}
        for i, field in enumerate(candidates):
            field_map[list(field)[0]] = i

        return field_map


def part1(input_data):
    rules, your_ticket, nearby_tickets = input_data.split("\n\n")
    validator = TicketValidator(rules)

    error_rate = 0
    for t in nearby_tickets.split("\n")[1:]:
        if not t:
            continue
        error_rate += sum(validator.scanning_error_rate(t))
    return error_rate


def part2(input_data):
    stanzas = input_data.split("\n\n")
    rules = stanzas[0]
    your_ticket = stanzas[1].split("\n")[1]
    nearby_tickets = stanzas[2].split("\n")[1:]

    validator = TicketValidator(rules)
    field_map = validator.identify_ticket_fields(nearby_tickets)

    # field_map now includes an authoritative map of which
    # fields (by name) map to which ticket columns.
    #
    # Now calculate the product of all fields on your_ticket which
    # start with "departure".
    
    columns = [c for k, c in field_map.items() if k.startswith("departure")]
    product = 1
    your_ticket_values = [int(x) for x in your_ticket.split(",")]
    for c in columns:
        product *= your_ticket_values[c]
    return product


if __name__ == "__main__":
    input_data = get_puzzle_input("input.txt")
    print(part2(input_data))
