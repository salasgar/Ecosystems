from basic_tools import is_number, is_dict, is_function
from basic_tools import dictionary_to_string, extract_all_strings
from basic_tools import print_reserves, print_methods_names
from basic_tools import print_costs, print_organism
from basic_tools import print_trade_transactions
from basic_tools import random_true, shuffle
from basic_tools import deep_copy_of_a_dictionary
from basic_tools import print_births, print_killed
from basic_tools import print_deths
from basic_tools import DEFAULT


actions_dictionary = {
    'do photosynthesis': lambda organism: organism.do_photosynthesis(),
    'move': lambda organism: organism.move(),
    'hunt': lambda organism: organism.hunt(),
    'interchange substances with other organisms': lambda organism:
        organism.interchange_substances_with_other_organisms(),
    'fertilize other organisms': lambda organism:
        organism.fertilize_other_organisms(),
    'fertilize': lambda organism: organism.fertilize_other_organisms(),
    'procreate': lambda organism: organism.procreate(),
    'do internal changes': lambda organism: organism.do_internal_changes(),
    'stay alive': lambda organism: organism.stay_alive(),
    'age': lambda organism: organism.age()
}


class Organism(dict):

    def __init__(self, parent_ecosystem, organism_data={}):
        self.parent_ecosystem = parent_ecosystem
        for key in organism_data:
            self[key] = organism_data[key]
        if 'metabolic time' in self:
            self.evolve = self.act_with_metabolic_time
        else:
            self.evolve = self.act

    def to_string(self, data):
        if is_number(data):
            return round(float(data), 2).__str__()
        elif is_dict(data):
            return dictionary_to_string(data)
        elif is_function(data):
            return self.to_string(data(self))
        elif hasattr(data, '__iter__'):
            return (self.to_string(item) for item in data)
        else:
            return data.__str__()

    # Just for debug
    def __str__(self, indent_level=0, list_of_attributes=None):
        if (list_of_attributes is None) or len(list_of_attributes) == 0:
            return dictionary_to_string(self, indent_level)
        else:
            if isinstance(list_of_attributes, str):
                return list_of_attributes, self.to_string(
                    self[list_of_attributes])
            elif len(list_of_attributes) == 1:
                return list_of_attributes[0], self.to_string(
                    self[list_of_attributes[0]])
            else:

                return ", ".join(
                    "{0}: {1}".format(attribute, self[attribute])
                    for attribute in list_of_attributes if attribute in self)

    def check_new_gene(self, gene_name, all_genes_settings):
        """
            If in the definition of the gene gene_name
            is there a mention to a gene that hasn't
            yet been initialized, gene_name can't still
            be initialized until all genes that it
            refers to are initialized.
            This function says whether gene_name can
            be already initialized or not.
        """
        all_strings = extract_all_strings(
            all_genes_settings[gene_name]['initial value'])
        if 'allowed interval' in all_genes_settings[gene_name]:
            all_strings = all_strings.union(
                extract_all_strings(
                    all_genes_settings[gene_name]['allowed interval']))
        for item in all_strings:
            if item in all_genes_settings and item not in self:
                # default_error_messenger('In', gene_name, 'failed', item)
                return False
        return True

    def is_reserve_substance(self, gene_name):
        return len(gene_name) > 8 and gene_name[-8:] == ' reserve'

    def add_gene(self, gene_name, gene_settings):
        # print "Adding gene", gene_name # ***
        functions = self.parent_ecosystem.function_maker.\
            turn_settings_into_functions(
                gene_settings,
                caller='#organism')
        self[gene_name] = functions['initial value'](self)
        if 'value after mutation' in gene_settings:
            self['value after mutation'][
                gene_name] = functions['value after mutation']
        if 'value in next cycle' in gene_settings:
            self['value in next cycle'][
                gene_name] = functions['value in next cycle']
        if self.is_reserve_substance(gene_name):
            self['list of reserve substances'].append(gene_name)
        if 'offer to sell' in gene_settings:
            self['offers to sell'][
                gene_name] = functions['offer to sell']

    def add_decision(self, decision_name, decision_settings):
        self[decision_name] = self.parent_ecosystem.function_maker.\
            read_function_settings(
            '#organism ' + decision_name,
            decision_settings
        )

    def configure_with_category_settings(self, category_settings):
        # Adding genes:
        all_genes_settings = category_settings['genes'] if \
            'genes' in category_settings else {}
        self['list of reserve substances'] = []
        self['value in next cycle'] = {}
        self['value after mutation'] = {}
        self['offers to sell'] = {}
        progressing = True
        while progressing:
            progressing = False
            for gene_name in all_genes_settings:
                if (
                    gene_name not in self and
                    self.check_new_gene(gene_name, all_genes_settings)
                ):
                    self.add_gene(gene_name, all_genes_settings[gene_name])
                    progressing = True
        # Adding decisions:
        all_decisions_settings = category_settings['decisions'] if \
            'decisions' in category_settings else {}
        for decision in all_decisions_settings:
            self.add_decision(decision, all_decisions_settings[decision])
        if 'metabolic time' in self:
            self.evolve = self.act_with_metabolic_time
        else:
            self.evolve = self.act

    def act_with_metabolic_time(self):
        while (
            self['metabolic time'] > 0 and
            self not in self.parent_ecosystem.new_deads
                ):
            self.act()
            self['metabolic time'] -= 1.0
        self['metabolic time'] = self['value in next cycle'][
            'metabolic time'](self)

    def act(self):
        if print_methods_names:  # ***
            print 'act'
        if print_reserves:  # ***
            print 'begin:',
            for reserve_substance in self['list of reserve substances']:
                print reserve_substance, self[reserve_substance],
            print ''
        # print self['actions list'] # ***
        actions_sequence = self['actions sequence']
        for action in actions_sequence:
            decision_name = 'decide ' + action
            if (
                (
                    decision_name in self and
                    self[decision_name](self)
                )
                or decision_name not in self
                    ):
                constraints = self.parent_ecosystem.constraints
                constraint_name = 'can ' + action
                if (
                    (constraint_name in constraints) and constraints[
                        constraint_name](self)
                ) or (constraint_name not in constraints):
                    actions_dictionary[action](self)
        if print_reserves:  # ***
            for reserve_substance in self['list of reserve substances']:
                print reserve_substance, self[reserve_substance],
            print ''
        if self.parent_ecosystem.constraints['die'](self):
            # print "dying alone", self.__str__(list_of_attributes =
            # ('category', 'age', 'energy reserve')) # ***
            self.die('Natural deth')

    def subtract_costs(self, action, tags_dictionary={}):
        if print_methods_names or print_costs:
            print 'subtract_costs', action  # ***
        if '#organism' not in tags_dictionary:
            tags_dictionary['#organism'] = self
        if action in self.parent_ecosystem.costs:
            costs = self.parent_ecosystem.costs[action]
            for reserve_substance in costs:
                if reserve_substance in self:
                    if print_costs:  # ***
                        print action + ":\n<-- ",
                        print_organism(
                            self, 'category', 'age', reserve_substance)
                    self[reserve_substance] = (
                        self[reserve_substance] -
                        costs[reserve_substance](tags_dictionary)
                        )
                    if self[reserve_substance] < 0 and action != 'die':
                        self.die(
                            'Natural deth: Starvation ' + reserve_substance)
                        if print_costs:
                            print 'Cost', action, reserve_substance,
                            print costs[reserve_substance](tags_dictionary),
                            print 'over reserve',
                            print reserve_substance, self[reserve_substance]
                        return 'deth'

                    if print_costs:  # ***
                        print "--> ",
                        print_organism(
                            self, 'category', 'age', reserve_substance)

    def buy_substance(
            self,
            seller,
            substance_to_sell,
            substance_to_buy_with,
            amount
            ):
        self[substance_to_sell] += amount
        seller[substance_to_sell] -= amount
        price = seller['offers to sell'][substance_to_sell][
            'prices'][substance_to_buy_with](seller)
        self[substance_to_buy_with] -= amount * price
        seller[substance_to_buy_with] += amount * price
        if random_true(print_trade_transactions):
            print '\nTrade:', amount, substance_to_sell, 'for',
            print amount * price, substance_to_buy_with, 'price:', price, "\n"

    def find_matching_trade_offers(self, seller):
        if seller is None or 'offers to sell' not in seller:
            return False
        seller_offers = seller['offers to sell']
        self_offers = self['offers to sell']
        matching_offers_list = []
        for substance_to_sell in seller_offers:
            for substance_to_buy_with in self_offers:
                seller_prices = seller_offers[substance_to_sell]['prices']
                self_prices = self_offers[substance_to_buy_with]['prices']
                if (
                    substance_to_sell in self_prices and
                    substance_to_buy_with in seller_prices and
                    seller_prices[substance_to_buy_with](seller) <
                    1.0 / self_prices[substance_to_sell](self)
                ):
                    price = seller_prices[substance_to_buy_with](seller)
                    amount = min(
                        seller_offers[substance_to_sell][
                            'amount'](seller),
                        self_offers[substance_to_buy_with][
                            'amount'](self) / price
                    )
                    if amount > 0:
                        matching_offer = (
                            substance_to_sell,
                            substance_to_buy_with,
                            amount
                        )
                        matching_offers_list.append(matching_offer)
        return matching_offers_list

    def trade_with(self, seller):
        # Find offers:
        matching_offers_list = self.find_matching_trade_offers(seller)
        # Chose one of the offers:
        if len(matching_offers_list) > 0:
            shuffle(matching_offers_list)
            for offer in matching_offers_list:
                (
                    substance_to_sell,
                    substance_to_buy_with,
                    amount
                ) = offer
                if amount > 0:
                    # Do the transaction:
                    self.buy_substance(
                        seller,
                        substance_to_sell,
                        substance_to_buy_with,
                        amount
                        )
                    # Subtract costs (pay taxes):
                    """
                        Para acelerar esta parte del codigo podemos utilizar
                        self.parent_ecosystem.costs[
                            'interchange substances with other organisms'][
                                'tags list']
                        para construir solamente la parte de tags_dictionary
                        que se vaya a usar:
                    """
                    tags_dictionary = {
                        '#organism': self,
                        '#seller': seller,
                        '#substance_to_sell': substance_to_sell,
                        '#substance_to_buy_with': substance_to_buy_with,
                        '#amount': amount,
                        '#distance': self.parent_ecosystem.biotope.distance(
                            self['location'],
                            seller['location']
                            )
                        }
                    self.subtract_costs(
                        'interchange substances with other organisms',
                        tags_dictionary
                        )
                    # A transaction has been made:
                    return True
                    # We can execute only one of the offers, because once it is
                    # done, the rest of offers may probably be obsolete
        return False

    def interchange_substances_with_other_organisms(self):
        # if print_methods_names: # ***
        #   print 'interchange_substances_with_other_organisms'

        """
        Peacefull trade of substances:
            Each organism has a list of offers for other organisms that can
        buy or not. An organism may want to sell its surplus of certain
        substances in exchange for other substances that it needs. It offers an
        amount of substance and a price (i. e. a ratio) in terms of other
        substance.
        """
        try:
            trade_radius = self['trade radius']
        except Exception:
            trade_radius = DEFAULT.trade_radius

        def condition(organism):
            return organism is not None and organism != self

        seller_location = self.parent_ecosystem.biotope.seek_organism_close_to(
            center=self['location'],
            radius=trade_radius,
            condition=condition
            )

        if seller_location is not None:
            seller = self.parent_ecosystem.biotope.\
                get_organism(seller_location)
            self.trade_with(seller)

    def inject_or_extract_susbtances_from_other_organisms(self):
        """
        Not so pacefull interchange of substances:
            An organism can stole a part of substance
        reserves from other organisms,
        as herbivorous do with plants, or as parasites
        do with their hosts.
            An organism may also inject a substance
        to other organism in order
        to kill it or damage it in self-defense of to
        eat it after it dies.
        """
        pass

    def fertilize_other_organisms(self):
        # if print_methods_names: # ***
        #   print 'fertilize_other_organisms'
        """ To partially transmit its own genes to
        other organisms that
        accepts them in order to produce a new being
        that inherit genes from
        both parents
        """
        pass

    def stay_alive(self):
        if print_methods_names or print_costs:  # ***
            print 'stay_alive'
        # print self['energy reserve'], self['photosynthesis capacity'],
        # "*****", self['actions sequence'](self)
        """ An organism has to spend energy and maybe
        other substances only to
        stay alive.
        """
        if 'stay alive' in self.parent_ecosystem.costs:
            tags_dictionary = {
                '#organism': self
            }
            self.subtract_costs('stay alive', tags_dictionary)

    def move(self):
        if print_methods_names:  # ***
            print 'move'
        """
            Check if there is a new available location. If yes
            then: - Update biotope (organisms matrix)
                  - Update location
        """
        # 1. Get a new location:
        new_location = self.parent_ecosystem.biotope.\
            seek_free_location_close_to(
                center=self['location'],
                radius=self['speed'])
        # 2. Check if it has found a new location:
        if new_location is not None:
            old_location = self['location']
            # 3. Update location
            self['location'] = new_location
            # 4. Update biotope (organisms matrix):
            self.parent_ecosystem.biotope.move_organism(
                old_location, new_location)
            # 5. The costs may be proportional to the distance we have jump,
            # or even the substances that there are in the biotope:
            tags_dictionary = {
                '#organism': self,
                '#distance': self.parent_ecosystem.biotope.distance(
                    old_location,
                    new_location),
                '#x': old_location[0],
                '#y': old_location[1]
            }
            self.subtract_costs('move', tags_dictionary)
            return 'moved to', new_location
        return "It didn't move"

    def move2(self):
        """
            Check if there is a new available location. If yes
            then: - Update biotope (organisms matrix)
                  - Update location
        """
        # No todos los organismos tienen por que usar la funcion
        # "seek_free_location_close_to(center, radius)" para buscar un sitio
        # al que moverse. Algun organismo puede usar una funcion mas
        # inteligente, que dependa de la concentracion de determinada
        # sustancia o del gradiente de densidad de poblacion de determinada
        # especie. O tambien puede haber otros que decidan moverse siempre en
        # linea recta hasta que se topen con algo. Hay infinidad de maneras de
        # moverse.

        # Por eso podriamos usar este metodo en lugar del anterior. La dejo
        # aqui por si lo usamos en un futuro. Esta es una forma alternativa de
        # definir el movimiento. Lo considera un cambio de estado como otro
        # cualquiera. Un organismo puede ser capaz de moverse de una
        # determinada manera al igual que otro organismo puede ser capaz de
        # cambiar cualquier otro gen interno de alguna otra manera.

        # Tenemos que decidir si usamos este metodo move o el anterior. La
        # unica diferencia para el usuario seria la manera de definir el
        # movimiento en ecosystem_settings

        # 1. Check if this organism can move itself:
        if 'location' in self['variable genes']:
            # 2. Check if this organism decide to move:
            if self['variable genes']['location']['will change?'](self):
                # 3. Get a new location:
                new_location = self['variable genes'][
                    'location']['new value'](self)
                # 4. Check if it has found a new location:
                if new_location is not None:
                    old_location = self['location']
                    # 5. Update location
                    self['location'] = new_location
                    # 6. Update biotope (organisms matrix):
                    self.parent_ecosystem.biotope.move_organism(
                        old_location, new_location)
                    # 7. The costs are proportional to the distance we have
                    # jump or the substances that there are in the biotope:
                    tags_dictionary = {
                        '#organism': self,
                        '#distance': self.parent_ecosystem.biotope.distance(
                            old_location,
                            new_location),
                        '#x': old_location[0],
                        '#y': old_location[1]
                    }
                    self.subtract_costs('move', tags_dictionary)

    def eat(self, prey):
        if print_methods_names:  # ***
            print 'eat'
        for reserve_substance in prey['list of reserve substances']:
            if reserve_substance in self:
                # print 'eating', prey['category'], self[reserve_substance],
                # "+", prey[reserve_substance], "=", # ***
                self[reserve_substance] += prey[reserve_substance]
                storage_capacity = reserve_substance[:-7] + 'storage capacity'
                if storage_capacity in self:
                    self[reserve_substance] = min(
                        self[reserve_substance], self[storage_capacity])
                # print self['energy reserve'] # ***
        tags_dictionary = {
            '#organism': self,
            '#prey': prey
        }
        self.subtract_costs('eat', tags_dictionary)

    def hunt(self):
        def check_if_prey_is_not_self(prey):
            return (prey is not None) and (prey != self)

        def check_if_self_decide_attack_prey(prey):
            return (prey is not None) and (
                    prey != self) and self['decide attack #prey'](self, prey)

        if print_methods_names:  # ***
            print 'hunt'
        prey_location = None
        if 'seeking prey technique' in self:
            prey_location = self['seeking prey technique'](self)
        else:
            if 'decide attack #prey' in self:
                condition = check_if_self_decide_attack_prey
            else:
                condition = check_if_prey_is_not_self
            try:
                hunt_radius = self['hunt radius']
            except Exception:
                hunt_radius = 1.5
            prey_location = self.parent_ecosystem.biotope.\
                seek_organism_close_to(
                    center=self['location'],
                    radius=hunt_radius,
                    condition=condition)
        if prey_location is not None:
            prey = self.parent_ecosystem.biotope.get_organism(prey_location)
            if self.parent_ecosystem.constraints['can kill #prey'](self, prey):
                self.eat(prey)
                prey.die('Killed by a predator')
                hunt_was_successful = True
                result = 'successful hunt'
            else:
                hunt_was_successful = False
                result = 'hunt failed, prey won'
            tags_dictionary = {
                '#organism': self,
                '#prey': prey,
                '#distance': self.parent_ecosystem.biotope.distance(
                    self['location'],
                    prey_location),
                '#hunt_was_successful': hunt_was_successful
            }
            self.subtract_costs('hunt', tags_dictionary)
        else:
            result = 'hunt failed, prey not found'
        return result

    def mutate(self):
        if print_methods_names:
            print 'mutate'  # ***
        for gene in self['value after mutation']:
            # print "MUTATING", gene # ***
            self[gene] = self['value after mutation'][gene](self)

    def do_internal_changes(self):
        if print_methods_names:
            print 'do_internal_changes'  # ***
        energy_reserve = self['energy reserve']  # this is for debuggin

        for gene in self['value in next cycle']:
            # print 'do_internal_changes', gene # ***
            if gene != 'metabolic time':
                self[gene] = self['value in next cycle'][gene](self)

        # print 'energy reserve: {0} + {1} = {2}'.format(energy_reserve,
        # self['energy reserve'] - energy_reserve, self['energy reserve']) #
        # ***
        # this is for debuggin purposes
        return 'energy reserve: {0} + {1} = {2}'.format(
            energy_reserve,
            self['energy reserve'] - energy_reserve,
            self['energy reserve'])

    def procreate(self):
        if print_methods_names:
            print 'procreate'  # ***
        """
            Depending on the reproduction frequency and the energy,
            a baby can be created and added to:
              - the organisms matrix in biotope
              - the list of organisms in parent_ecosystem
            Return true if procreated, else return false.
        """

        if ('can procreate' in self.parent_ecosystem.constraints and
                not self.parent_ecosystem.constraints['can procreate'](self)):
            return False
        elif ('decide procreate' in self and
              not self['decide procreate'](self)):
            return False

        procreated = False
        # Get a new location for the new baby:
        try:
            radius_of_procreation = self['radius of procreation']
        except Exception:
            radius_of_procreation = 1.5
        new_location = self.parent_ecosystem.biotope.\
            seek_free_location_close_to(
                center=self['location'], radius=radius_of_procreation)
        if new_location is not None:  # if there is enough space:
            # Create the baby:
            # print 'making a deep copy'  # ***
            newborn = Organism(
                self.parent_ecosystem, deep_copy_of_a_dictionary(self))
            """
            # Utilizamos deep_copy_of_a_dictionary, porque es mucho mas
            veloz que deepcopy()
            Esto genera un enorme cuello de botella, ralentizando mucho
            el programa
            """
            newborn['location'] = new_location
            if 'age' in newborn:
                newborn['age'] = 0
            # Trigger mutations:
            newborn.mutate()
            # The parent and the child share reserves:
            if 'energy reserve' in self:
                newborn['energy reserve'] = newborn['energy reserve at birth']
            for reserve_substance in self['list of reserve substances']:
                self[reserve_substance] -= newborn[reserve_substance]
            # Add the new organism to the ecosystem:
            self.parent_ecosystem.add_organism(newborn)
            tags_dictionary = {
                '#organism': self,
                '#newborn': newborn,
                '#distance': self.parent_ecosystem.biotope.distance(
                    self['location'],
                    new_location)
            }
            self.subtract_costs(
                'procreate',
                tags_dictionary)
            procreated = True
            if print_births:       # ***
                # print 'SELF:'
                # print_dictionary(self)
                # print "\nNEWBORN:"
                # print_dictionary(newborn)
                # a = raw_input('press any key...')
                print "newborn!",
        # else:
            # print "Not enough space" # ***
        return procreated

    def die(self, cause='natural deth'):
        if print_methods_names:
            print 'die'  # ***
        # self.parent_ecosystem.delete_organism(self) # parent_ecosystem tells
        # biotope to erase organism from it
        if print_deths:     # ***
            print 'dying', self.__str__(
                list_of_attributes=(
                    'category',
                    'age',
                    'energy reserve'
                    )
                ), cause
        elif print_killed and cause == 'Killed by a predator':  # ***
            print 'dying', self.__str__(
                list_of_attributes=(
                    'category',
                    'age',
                    'energy reserve')
                ), cause
        self.subtract_costs('die', {'#organism': self, '#cause': cause})
        self.parent_ecosystem.new_deads.append(self)
