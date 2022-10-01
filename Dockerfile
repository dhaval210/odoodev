FROM eu.gcr.io/cf-rungis-exp-development-4l/odoofinal
MAINTAINER LNKAsia Techsol LLP. <support@lnkasia.com>

# Copy Odoo configuration file
COPY ./odoo.conf /etc/odoo/

# Setting up code directory
COPY /development/ /mnt/transfer/
RUN rename /mnt/transfer/* /mnt/transfer/sale_discount_limit
RUN ls -l /mnt/transfer/
# Expose Odoo services
EXPOSE 8069 8071 8072

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]