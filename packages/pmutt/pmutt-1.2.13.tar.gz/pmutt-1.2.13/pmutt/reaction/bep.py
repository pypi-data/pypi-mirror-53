# -*- coding: utf-8 -*-
from pmutt import _ModelBase
from pmutt import constants as c
from pmutt.io.json import remove_class


class BEP(_ModelBase):
    """Represents a Bronsted Evans Polyani relationship. Intended to be a
    ``specie`` class.

    :math:`E_a = \\alpha H + \\beta`

    Attributes
    ----------
        slope : float
            Slope of BEP relationship.
        intercept : float
            Intercept of BEP relationship in kcal/mol.
        name : str, optional
            Name of the BEP. Default is None
        reaction : :class:`~pmutt.reaction.Reaction` object, optional
            Reaction related to BEP. The Reaction can be supplied later by
            using ``set_descriptor``
        descriptor : str, optional
            Descriptor to calculate the activation energy. Supported options:

            ===========  ===========================================================================
            Descriptor   Description
            ===========  ===========================================================================
            delta_H      H_products - H_reactants (change in enthalpy)
            rev_delta_H  H_reactants - H_products (change in enthalpy in reverse direction)
            reactants_H  H_reactants (enthalpy of reactants)
            products_H   H_products (enthalpy of products)
            delta_E      E_products - E_reactants (change in electronic energy)
            rev_delta_E  E_reactants - E_products (change in electronic energy in reverse direction)
            reactants_E  E_reactants (electronic energy of reactants)
            products_E   E_products (electronic energy of products)
            ===========  ===========================================================================

            Default is 'delta_H'.
        notes : str or dict
            Notes relevant to BEP relationship such as its source. If using a
            dictionary, the keys and values must be simple types supported by
            JSON
        _descriptor : method
            Method taken from reaction to calculate enthalpy. This attribute is
            not supplied to constructor.
    """

    def __init__(self, slope, intercept, name=None, reaction=None,
                 descriptor='delta_H', notes=None):
        self.name = name
        self.slope = slope
        self.intercept = intercept
        self.descriptor = descriptor
        self.reaction = reaction
        self.notes = notes
    
    @property
    def reaction(self):
        return self._reaction

    @reaction.setter
    def reaction(self, val):
        self._reaction = val
        self._set_descriptor_fn(reaction=val)

    @property
    def descriptor(self):
        return self._descriptor
    
    @descriptor.setter
    def descriptor(self, val):
        if val is not None:
            self._descriptor = val
            self._set_descriptor_fn(descriptor=val)


    def _set_descriptor_fn(self, reaction=None, descriptor=None):
        """Sets the appropriate method handle to the BEP object

        Parameters
        ----------
            reaction : :class:`~pmutt.reaction.Reaction` object, optional
                Reaction related to BEP. If specified, overwrites the value
                held by BEP object
            descriptor : str, optional
                Descriptor to calculate the activation energy. Supported
                options:

                ===========  ===========================================================================
                Descriptor   Description
                ===========  ===========================================================================
                delta_H      H_products - H_reactants (change in enthalpy)
                rev_delta_H  H_reactants - H_products (change in enthalpy in reverse direction)
                reactants_H  H_reactants (enthalpy of reactants)
                products_H   H_products (enthalpy of products)
                delta_E      E_products - E_reactants (change in electronic energy)
                rev_delta_E  E_reactants - E_products (change in electronic energy in reverse direction)
                reactants_E  E_reactants (electronic energy of reactants)
                products_E   E_products (electronic energy of products)
                ===========  ===========================================================================
                
                If specified, overwites the value held by BEP object.
        """
        # Return if the descriptor has not been set or is None
        try:
            self.descriptor
        except AttributeError:
            return
        else:
            if self.descriptor is None:
                return

        # Return if the reaction has not been set or is None
        try:
            self.reaction
        except AttributeError:
            return
        else:
            if self.reaction is None:
                return   

        # Assign the descriptor to the reaction
        if self.descriptor == 'delta_H':
            self._descriptor_fn = \
                    lambda **kwargs: self.reaction.get_delta_H(rev=False,
                                                               units='kcal/mol',
                                                               **kwargs)
        elif self.descriptor == 'rev_delta_H':
            self._descriptor_fn = \
                    lambda **kwargs: self.reaction.get_delta_H(rev=True,
                                                               units='kcal/mol',
                                                               **kwargs)
        elif self.descriptor == 'reactants_H':
            self._descriptor_fn = \
                    lambda **kwargs: self.reaction.get_H_state(
                            units='kcal/mol',
                            state='reactants',
                            **kwargs)
        elif descriptor == 'products_H':
            self._descriptor_fn = \
                    lambda **kwargs: self.reaction.get_H_state(
                            units='kcal/mol',
                            state='products',
                            **kwargs)
        elif self.descriptor == 'delta_E':
            self._descriptor_fn = \
                    lambda **kwargs: self.reaction.get_delta_E(rev=False,
                                                               units='kcal/mol',
                                                               **kwargs)
        elif self.descriptor == 'rev_delta_E':
            self._descriptor_fn = \
                    lambda **kwargs: self.reaction.get_delta_E(rev=True,
                                                               units='kcal/mol',
                                                               **kwargs)
        elif self.descriptor == 'reactants_E':
            self._descriptor_fn = \
                    lambda **kwargs: self.reaction.get_E_state(
                            units='kcal/mol',
                            state='reactants',
                            **kwargs)
        elif self.descriptor == 'products_E':
            self._descriptor_fn = \
                    lambda **kwargs: self.reaction.get_E_state(
                            units='kcal/mol',
                            state='products',
                            **kwargs)
        else:
            err_msg = ('Descriptor "{}" not supported. See documentation of '
                       'pmutt.reaction.bep.BEP for supported options.'
                       ''.format(self.descriptor))
            raise ValueError(err_msg)

    def get_E_act(self, units, rev=False, **kwargs):
        """Calculate Arrhenius activation energy using BEP relationship

        Parameters
        ----------
            units : str
                Units as string. See :func:`~pmutt.constants.R` for accepted
                units but omit the '/K' (e.g. J/mol).
            rev : bool, optional
                Reverse direction. If True, uses products as initial state
                instead of reactants. Default is False
            kwargs : keyword arguments
                Parameters required to calculate the descriptor
        Returns
        -------
            E_act : float
                Dimensionless activation energy
        """
        if 'rev_delta' in self.descriptor:
            # If the descriptor is for the reverse reaction, the slope has to
            # be modified
            if rev:
                E_act = self.slope*self._descriptor_fn(**kwargs) + self.intercept
            else:
                E_act = (self.slope-1.)*self._descriptor_fn(**kwargs) \
                        + self.intercept
        else:
            if rev:
                E_act = (self.slope-1.)*self._descriptor_fn(**kwargs) \
                        + self.intercept
            else:
                E_act = self.slope*self._descriptor_fn(**kwargs) + self.intercept
        return E_act*c.convert_unit(initial='kcal/mol', final=units)

    def get_EoRT_act(self, rev=False, T=c.T0('K'), **kwargs):
        """Calculates dimensionless Arrhenius activation energy using BEP
        relationship

        Parameters
        ----------
            rev : bool, optional
                Reverse direction. If True, uses products as initial state
                instead of reactants. Default is False
            T : float, optional
                Temperature in K. Default is 298.15
            kwargs : keyword arguments
                Parameters required to calculate the descriptor
        Returns
        -------
            EoRT_act : float
                Dimensionless activation energy
        """
        return self.get_E_act(units='kcal/mol', rev=rev, T=T, **kwargs) \
               /c.R('kcal/mol/K')/T

    def get_UoRT(self, T=c.T0('K'), **kwargs):
        """Calculates the dimensionless internal energy using BEP relationship
        and initial state internal energy
        
        Parameters
        ----------
            T : float, optional
                Temperature in K. Default is 298.15
            kwargs : keyword arguments
                Parameters required to calculate the descriptor
        Returns
        -------
            UoRT : float
                Dimensionless internal energy
        """
        UoRT_reactants = self.reaction.get_UoRT_state(state='reactants', T=T,
                                                      **kwargs)
        return self.get_EoRT_act(rev=True, T=T, **kwargs) + UoRT_reactants

    def get_HoRT(self, T=c.T0('K'), **kwargs):
        """Calculates the dimensionless enthalpy using BEP relationship
        and reactants or products enthalpy
        
        Parameters
        ----------
            T : float, optional
                Temperature in K. Default is 298.15
            kwargs : keyword arguments
                Parameters required to calculate the descriptor
        Returns
        -------
            HoRT : float
                Dimensionless enthalpy
        """
        HoRT_reactants = self.reaction.get_HoRT_state(state='reactants', T=T,
                                                      **kwargs)
        return self.get_EoRT_act(rev=False, T=T, **kwargs) + HoRT_reactants

    def get_SoR(self, T=c.T0('K'), entropy_state='reactants', **kwargs):
        """Calculates the dimensionless entropy using reactants or products
        entropy. The BEP relationship has no entropic contribution
        
        Parameters
        ----------
            T : float, optional
                Temperature in K. Default is 298.15
            entropy_state : str or None, optional
                State to use to estimate entropy. Supported arguments:

                - 'reactants' (default)
                - 'products'
                - None (Entropy contribution is 0. Useful if misc_models
                  have been specified for entropy)
            kwargs : keyword arguments
                Parameters required to calculate the descriptor
        Returns
        -------
            SoR : float
                Dimensionless entropy
        """
        if entropy_state is None:
            SoR = 0.
        else:
            SoR = self.reaction.get_SoR_state(state=entropy_state, T=T,
                                              **kwargs)
        return SoR

    def get_GoRT(self, T=c.T0('K'), entropy_state='reactants', **kwargs):
        """Calculates the dimensionless Gibbs energy using BEP relationship
        and reactants Gibbs energy. The BEP relationship has no entropic
        contribution
        
        Parameters
        ----------
            T : float, optional
                Temperature in K. Default is 298.15
            entropy_state : str or None, optional
                State to use to estimate entropy. Supported arguments:

                - 'reactants' (default)
                - 'products'
                - None (Entropy contribution is 0. Useful if misc_models
                  have been specified for entropy)
            kwargs : keyword arguments
                Parameters required to calculate the descriptor
        Returns
        -------
            GoRT : float
                Dimensionless Gibbs energy
        """
        return self.get_HoRT(T=T, **kwargs) \
               - self.get_SoR(T=T, entropy_state=entropy_state, **kwargs)

    def to_dict(self):
        """Represents object as dictionary with JSON-accepted datatypes

        Returns
        -------
            obj_dict : dict
        """
        obj_dict = {
            'class': str(self.__class__),
            'name': self.name,
            'slope': self.slope,
            'intercept': self.intercept,
            'descriptor': self.descriptor,
            'notes': self.notes}
        return obj_dict