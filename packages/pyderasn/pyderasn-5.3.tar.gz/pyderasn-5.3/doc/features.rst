Features
========

* BER/CER/DER decoding, DER encoding
* Basic ASN.1 data types (X.208): BOOLEAN, INTEGER, BIT STRING, OCTET
  STRING, NULL, OBJECT IDENTIFIER, ENUMERATED, all strings, UTCTime,
  GeneralizedTime, CHOICE, ANY, SEQUENCE (OF), SET (OF)
* Size :ref:`constraints <bounds>` checking
* Working with sequences as high level data objects with ability to
  (un)marshall them
* Python 2.7/3.5/3.6 compatibility
* Aimed to be complaint with `X.690-201508 <https://www.itu.int/rec/T-REC-X.690-201508-I/en>`__

Why yet another library? `pyasn1 <http://snmplabs.com/pyasn1/>`__
had all of this a long time ago. PyDERASN resembles it in many ways. In
practice it should be relatively easy to convert ``pyasn1``'s code to
``pyderasn``'s one.
Also there is `asn1crypto <https://github.com/wbond/asn1crypto>`__.

* Small, simple and trying to be reviewable code. Just a single file
  with `six <https://pypi.org/project/six/>`__ dependency
* Ability to know :ref:`exact decoded <decoding>` objects offsets and
  lengths inside the binary
* Automatic decoding of :ref:`DEFINED BY <definedby>` fields
* Ability to know exact decoded field presence, emptiness: for example
  ``SEQUENCE`` can lack ``OPTIONAL SEQUENCE OF`` field, but also can
  have it with no elements inside
* **Strict** DER-encoding checks. If whole input binary is parsed, then
  it must be completely valid DER-encoded structure
* Ability to allow BER-encoded data with knowing if any of specified
  field has either DER or BER encoding (or possibly indefinite-length
  encoding). For example
  `CMS <https://en.wikipedia.org/wiki/Cryptographic_Message_Syntax>`__
  structures allow BER encoding for the whole message, except for
  ``SignedAttributes`` -- you can easily verify your CMS satisfies that
  requirement
* Extensive and comprehensive
  `hypothesis <https://hypothesis.readthedocs.io/en/master/>`__
  driven tests coverage. It also has been fuzzed with
  `python-afl <http://jwilk.net/software/python-afl>`__
* Some kind of strong typing: SEQUENCEs require the exact **type** of
  settable values, even when they are inherited (assigning ``Integer``
  to the field with the type ``CMSVersion(Integer)`` is not allowed)
* However they do not require exact tags matching: IMPLICIT/EXPLICIT
  tags will be set automatically in the given sequence (assigning of
  ``CMSVersion()`` object to the field ``CMSVersion(expl=...)`` will
  automatically set required tags)
* Descriptive errors, like ``pyderasn.DecodeError: UTCTime
  (tbsCertificate:validity:notAfter:utcTime) (at 328) invalid UTCTime format``
* ``__slots__`` friendliness
* Could be significantly faster and have lower memory usage
  For example parsing of CACert.org's CRL (8.48 MiB) on FreeBSD 12.0
  amd64, Intel Core i5-6200U 2.3 GHz machine, Python 3.5.5/2.7.15:

  .. list-table::
     :widths: 15 45 20 20
     :header-rows: 1

     * - Library
       - Command
       - Time, sec (Py3/Py2)
       - Memory used, MiB (Py3/Py2)
     * - pyasn1 0.4.5
       - ``der_decode(data, asn1Spec=rfc5280.CertificateList())``
       - 1257 / 1302
       - 1327 / 2093
     * - asn1crypto 0.24.0
       - ``asn1crypto.crl.CertificateList.load(data).native``
       - 29.3 / 43.8
       - 983 / 1677
     * - pyderasn 4.9
       - ``CertificateList().decode(data)`` (CertificateList is
         converted ``pyasn1`` scheme definition)
       - 27.6 / 32.5
       - 498 / 488
* :ref:`Pretty printer <pprinting>` and
  :ref:`command-line decoder <cmdline>`, that could
  conveniently replace utilities like either ``dumpasn1`` or
  ``openssl asn1parse``

  .. figure:: pprinting.png
     :alt: Pretty printing example output

     An example of pretty printed X.509 certificate with automatically
     parsed DEFINED BY fields.

There are drawbacks:

* No old Python versions support
* See :ref:`limitations <limitations>`
